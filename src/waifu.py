from pynput import keyboard

import chat
import os
import recorder
import transcriber

OPENAI_API_KEY_FILE = "openai_key"
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
		self.primer = "simulate a conversation with 2 people, friend and wAIfu. wAIfu is a kind, clever, witty, friendly, and sometimes sarcastic person. They enjoy playing games and relaxing at home."

		self.conversation = list()
		return


	def load_waifu(self):
		self.whisper_client = transcriber.whisper_client()
		self.whisper_client.load("base")

		self.gpt_client = chat.gpt_client()
		self.gpt_client.load_api_key(OPENAI_API_KEY_FILE)
		self.gpt_client.load_model_gpt_3_5()

		self.voice_recorder = recorder.audio_recorder(WAVE_OUTPUT_FILE)
		return

	def run_chat_pipeline(self):
		prompt = ""
		# Transcribe user speech into text
		try:
			user_message = self.whisper_client.transcribe(WAVE_OUTPUT_FILE).strip()
			print("You: \"" + user_message + "\"")
		except err:
			print(err)
			return

		if user_message == "":
			return

		# Update conversation with user input
		self.conversation.append({ "role": "user", "content": "Friend: " + user_message })

		# OpenAI chat completion
		try:
			full_conversation = self.conversation
			full_conversation.insert(0, {"role": "system", "content": self.primer})
			response = self.gpt_client.chat(full_conversation)
			print(response)
		except err:
			print(err)
			return

		# Update conversation with wAIfu response
		self.conversation.append({ "role": "assistant", "content": "wAIfu: " + response })

		# Trim conversation if it gets too large
		if len(self.conversation) > self.memory_length:
			self.conversation = self.conversation[2:]

		# Save chat history to history file
		chat_file = open(CHAT_HISTORY_FILE, "a")
		chat_file.write("\nYou: " + user_message)
		chat_file.write("\nwAIfu: " + response)
		chat_file.close()

		# TODO integrate voice synthesis when added

		self.cleanup()

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
