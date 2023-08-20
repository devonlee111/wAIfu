from playsound import playsound
from pynput import keyboard

import json
import openai
import os
import requests

import recorder

# Local Program Information
CONFIG_FILE = "config.json"
WAVE_OUTPUT_FILE = "output.wav"
CHAT_HISTORY_FILE = "chat.history"
VOICE_OUTPUT_FILE = "response.wav"

# AI API Information
GPT_MODEL = "gpt-3.5-turbo"
GPT_TEMPERATURE = 1.0
GPT_FREQ_PENALTY = 2.0
GPT_PRES_PENALTY = 2.0

ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/"
CHUNK_SIZE = 1024

class waifu():
	def __init__(self):
		# Local voice recorder
		self.voice_recorder = None

		# AI API information
		self.eleven_labs_API_key = ""

		# Name assigned to the AI
		self.ai_name = ""

		# Name to refer to the user as
		self.user_name = ""

		# Prompt message used to prime the model before being given chat message(s)
		# This can be anything and can include such ideas as the AI's role, personality traits, disposition etc...
		# Larger prompt primer will be more costly when hitting the openAI API
		self.primer = ""

		# How many chat messages should be taken into consideration for the chat prompt
		# Larger memory length will be more costly when hitting the openAI API
		self.memory_length = 15

		# The chat message log stored in memory
		self.conversation = list()
		return

	# Load information required for operation
	def load_waifu(self):
		prompt_file = ""
		data = None

		# Load configs
		try :
			with open(CONFIG_FILE) as config_file:
				data = json.load(config_file)
				prompt_file = data["promptFile"]
				openai.api_key = data["openAIAPIKey"]
				self.eleven_labs_API_key = data["elevenLabsAPIKey"]
				self.eleven_labs_voice_ID = data["elevenLabsVoiceID"]
				self.ai_name = data["aiName"]
				self.user_name = data["userName"]
		except Exception as e:
			print("failed to load wAIfu configs...")
			print(e._message)
			quit(1)

		# Get primer prompt from prompt file
		file = open(prompt_file)
		self.primer = file.read().strip()
		file.close()

		# Perform final verifications
		if not self.verify_initial_waifu_configs():
			print("waifu configs verfification failed... exiting")
			exit(1)

		# Setup voice recorder
		self.voice_recorder = recorder.audio_recorder(WAVE_OUTPUT_FILE)

		return

	# Verify required configs are set
	def verify_initial_waifu_configs(self):
		verified = True
		if self.primer == "":
			print("no prompt primer found...")
			verified = False

		if openai.api_key == "":
			print("OpenAI API key has not been configured...")
			verified = False

		if self.eleven_labs_API_key == "":
			print("Eleven Labs API key has not been configured...")
			verified = False

		if self.eleven_labs_voice_ID == "":
			print("Eleven Labs voice ID has not been configured...")
			verified = False

		if self.ai_name == "":
			print("AI's name has not been configured...")
			verified = False

		if self.user_name == "":
			print("User's name has not been configured...")
			verified = False

		return verified

	# Transcribe user audio using OpenAI Whisper
	# Generate response to user using OpenAI GPT
	# Generate response audio using Eleven Labs
	# Play audio response to
	def run_chat_pipeline(self):
		# Transcribe user speech into text
		audio_file = open(WAVE_OUTPUT_FILE, "rb")

		# Use OpenAI Whisper to transcribe speech
		try:
			transcription = openai.Audio.transcribe("whisper-1", audio_file)
		except Exception as e:
			print("transcription failed")
			print(e.message)
			return

		user_message = transcription["text"].strip()

		if user_message == "":
			return

		print(f"{ self.user_name }: \"{ user_message }\"")

		# Update conversation with user input
		self.conversation.append({ "role": "user", "content": f"{ self.user_name }: { user_message }"})

		# OpenAI chat completion
		try:
			# Insert primer prompt into conversation every time
			processed_conversation = self.conversation
			processed_conversation.insert(0, {"role": "system", "content": self.primer})

			# Use OpenAI GPT Chat Completion to generate response
			response = openai.ChatCompletion.create(
				model = GPT_MODEL,
				messages = processed_conversation,
				temperature=GPT_TEMPERATURE,
				frequency_penalty=GPT_FREQ_PENALTY,
				presence_penalty=GPT_PRES_PENALTY,
				stop=["\n"]
			)
		except Exception as e:
			print(e._message)
			return

		waifu_response = response['choices'][0]['message']['content'].strip()
		print(waifu_response)

		# Update conversation with wAIfu response
		self.conversation.append({ "role": "assistant", "content": waifu_response })

		# Trim conversation if it gets too large
		if len(self.conversation) > self.memory_length:
			self.conversation = self.conversation[2:]

		# Save recent chat to history file
		chat_file = open(CHAT_HISTORY_FILE, "a")
		chat_file.write(f"\n{ self.user_name }: { user_message }")
		chat_file.write(f"\n{ self.ai_name }: { waifu_response } ")
		chat_file.close()

		waifu_response = waifu_response[len(f"{ self.ai_name }: "):]

		# Send response to Eleven Labs for voice synthesis
		try:
			# Eleven Labs API headers
			headers = {
				"Accept": "audio/mpeg",
				"Content-Type": "application/json",
				"xi-api-key": self.eleven_labs_API_key
			}

			# Eleven Labs API body
			data = {
				"text": waifu_response,
				"voice_settings": {
					"stability": 0,
					"similarity_boost": 0
				}
			}

			# Hit API and recieve response
			endpoint = ELEVENLABS_TTS_URL + self.eleven_labs_voice_ID
			response = requests.post(endpoint, json=data, headers=headers)

			# Save audio file response locally
			with open(VOICE_OUTPUT_FILE, 'wb') as f:
				for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
					if chunk:
						f.write(chunk)

			# Play response audio file
			playsound(VOICE_OUTPUT_FILE)

		except Exception as e:
			print(e._message)

		# Cleanup remnants
		self.cleanup()

	# Cleanup audio files
	def cleanup(self):
		os.remove(WAVE_OUTPUT_FILE)
		os.remove(VOICE_OUTPUT_FILE)
		return

	########## KEYBOARD INPUT STUFF ##########

	def on_press(self, key):
		if key.char == 'r':
			if not self.voice_recorder.recording:
				self.voice_recorder.start()
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
