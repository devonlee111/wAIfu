from pynput import keyboard
from playsound import playsound

import json
import os

import chat
import recorder
import transcriber
import voice

CONFIG_FILE = "config.json"
WAVE_OUTPUT_FILE = "output.wav"
CHAT_HISTORY_FILE = "chat.history"
VOICE_OUTPUT_FILE = "response.wav"

STT_ENGINE_WHISPER_LOCAL = "whisper local"
STT_ENGINE_WHISPER_API = "whisper api"

class waifu():
	def __init__(self):
		self.gpt_API_key = ""
		self.voice_recorder = None
		self.gpt_client = None
		self.listener = None
		self.voice = None

		# Name assigned to the AI
		self.ai_name = ""

		# Name to refer to the user as
		self.user_name = ""

		self.language = ""

		# Prompt message used to prime the model before being given chat message(s)
		# This can be anything and can include such ideas as the AI's role, personality traits, disposition etc...
		# Larger prompt primer will be more costly when hitting the openAI API
		self.primer = ""

		# How many chat messages should be taken into consideration for the chat prompt
		# Larger memory length will be more costly when hitting the openAI API
		self.memory_length = 15

		# The chat message log stored in memory
		self.conversation = list()

		# Voice file to attempt to clone
		# Only works for coqui YourTTS model
		self.voice_file = ""
		return

	def load_waifu(self):
		prompt_file = ""
		data = None
		voice_engine = ""
		tts_engine = ""

		# Load configs
		try :
			with open(CONFIG_FILE) as config_file:
				data = json.load(config_file)
				prompt_file = data["promptFile"]
				voice_engine = data["voiceEngine"]
				self.gpt_API_key = data["openAIGPTAPIKey"]
				self.ai_name = data["aiName"]
				self.user_name = data["userName"]
				self.language = data["language"]
				self.voice_clone_file = data["cloneVoiceFile"]
		except Exception as e:
			print("failed to load wAIfu configs...")
			print(e._message)
			quit(1)

		# Get prompt primer
		file = open(prompt_file)
		self.primer = file.read().strip()
		file.close()

		# Perform final verifications
		if not self.verify_initial_waifu_configs():
			exit(1)

		# Setup whisper client
		self.whisper_client = transcriber.whisper_client()
		self.whisper_client.use_local()
		whisper_model = data["whisperModel"]
		self.whisper_client.load(whisper_model, self.language)

		# Setup gpt client
		self.gpt_client = chat.gpt_client()
		self.gpt_client.load_api_key(self.gpt_API_key)
		self.gpt_client.load_model_gpt_3_5()

		# Setup voice recorder
		self.voice_recorder = recorder.audio_recorder(WAVE_OUTPUT_FILE)

		# Setup voice synthesizer
		coqui_speech_model = data["coquiSpeechModel"]
		if coqui_speech_model == "":
			print("A model is required for coqui speech synthesis, but none was provided...")
			exit(1)

		coqui_model_speaker = data["coquiModelSpeaker"]

		self.voice = voice.coqui_voice_synthesizer(model=coqui_speech_model, speaker=coqui_model_speaker, language=self.language, voice_to_clone=self.voice_clone_file)
		self.voice.load()

		# Perform final verifications
		# TODO fix this
		#if not self.verify_waifu_setup():
		#	exit(1)

		return

	def verify_initial_waifu_configs(self):
		if self.primer == "":
			print("no prompt primer found...")
			return False

		if self.gpt_API_key == "":
			print("OpenAI API key has not been configured...")
			return False

		if self.ai_name == "":
			print("AI's name has not been configured...")
			return False

		if self.user_name == "":
			print("User's name has not been configured...")
			return False

		if self.language == "":
			print("no language has been set...")
			return False

		return True

	def verify_waifu_setup(self):
		if self.whisper_client.model == "":
			print("Whisper voice recognition model has not been configured...")
			return False

		if self.voice.model == "":
			print("Coqui speech model has not been configured...")
			return False

		return True

	def run_chat_pipeline(self):
		prompt = ""
		# Transcribe user speech into text
		try:
			user_message = self.whisper_client.transcribe(WAVE_OUTPUT_FILE).strip()
			print(f"{ self.user_name }: \"{ user_message }\"")
		except Exception as e:
			print(e._message)
			return

		if user_message == "":
			return

		# Update conversation with user input
		self.conversation.append({ "role": "user", "content": f"{ self.user_name }: { user_message }"})

		# OpenAI chat completion
		try:
			full_conversation = self.conversation
			full_conversation.insert(0, {"role": "system", "content": self.primer})
			response = self.gpt_client.chat(full_conversation)
			print(response)
		except Exception as e:
			print(e._message)
			return

		# Update conversation with wAIfu response
		self.conversation.append({ "role": "assistant", "content": response })

		# Trim conversation if it gets too large
		if len(self.conversation) > self.memory_length:
			self.conversation = self.conversation[2:]

		# Save chat history to history file
		chat_file = open(CHAT_HISTORY_FILE, "a")
		chat_file.write(f"\n{ self.user_name }: { user_message }")
		chat_file.write(f"\n{ self.ai_name }: { response } ")
		chat_file.close()

		response = response[len(f"{ self.ai_name }: "):]
		try:
			self.voice.synthesize_speech(response, VOICE_OUTPUT_FILE)
			playsound(VOICE_OUTPUT_FILE)
		except Exception as e:
			print(e._message)

		self.cleanup()

	def cleanup(self):
		os.remove(WAVE_OUTPUT_FILE)
		os.remove(VOICE_OUTPUT_FILE)
		return

	def on_press(self, key):
		if key.char == 'r':
			if not self.voice_recorder.recording:
				self.voice_recorder.start()
				return True
			else:
				self.voice_recorder.stop()
				self.run_chat_pipeline()

			return True

		return False

	def on_release(self, key):
		return True

	def run(self):
		print("Press the 'r' key to begin recording")
		print("Press the 'r' key again to end recording")
		print("Press anything else to end the program")
		self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
		self.listener.start()
		self.listener.join()

if __name__ == "__main__":
	waifu = waifu()
	waifu.load_waifu()
	waifu.run()
