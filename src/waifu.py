from pynput import keyboard

import chat
import os
import recorder
import transcriber

OPENAI_API_KEY_FILE = "./openai_key"
WAVE_OUTPUT_FILE = "output.wav"
CHAT_HISTORY_FILE = "chat.history"

class waifu():
	def __init__(self):
		self.voice_recorder = None
		self.gpt_client = None
		self.whisper_client = None
		self.listener = None

		# How many chat messages should be taken into consideration for the chat prompt
		# Larger memory length will be more costly when hitting the openAI API
		self.memory_length = 50

		# Prompt message used to prime the model before being given chat message(s)
		# This can be anything and can include such ideas as the AI's role, personality traits, disposition etc...
		# Larger prompt primer will be more costly when hitting the openAI API
		self.prompt_primer = "wAIfu is a kind, clever, creative, and sometimes sarcastic friend"
		return


	def load_waifu(self):
		self.whisper_client = transcriber.whisper_client()
		self.whisper_client.load("base")

		self.gpt_client = chat.gpt_client()
		self.gpt_client.load_api_key(OPENAI_API_KEY_FILE)
		self.gpt_client.load_model_davinci()

		self.voice_recorder = recorder.audio_recorder(WAVE_OUTPUT_FILE)
		return

	def set_personality(self, personality):
		self.personality = personality
		return

	def run_chat_pipeline(self):
		prompt = ""
		# Transcribe user speech into text
		try:
			prompt = self.whisper_client.transcribe(WAVE_OUTPUT_FILE)
			print("You: \"" + prompt + "\"")
		except err:
			print(err)
			return

		if prompt == "":
			return

		# OpenAI chat completion
		try:
			full_prompt = self.prompt_primer + "\n\nYou: " + prompt + "\nwAIfu:"
			response = self.gpt_client.chat(prompt)
			print("wAIfu: \"" + response + "\"")
		except err:
			print(err)
			return

		# Save chat history to history file
		chat_file = open(CHAT_HISTORY_FILE, "a")
		chat_file.write("\nYou: " + prompt)
		chat_file.write("\nwAIfu: + response")
		chat_file.close()

		# TODO integrate voice synthesis when added

		self.cleanup()

	def build_prompt(self, prompt):
		final_prompt = prompt
		return final_prompt

	def cleanup(self):
		os.remove(WAVE_OUTPUT_FILE)
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

		return false

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
