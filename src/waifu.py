from pynput import keyboard

import chat
import recorder
import transcriber

OPENAI_API_KEY_FILE = "./openai_key"
WAVE_OUTPUT_FILE = "output.wav"

class waifu():
	def __init__(self):
		self.voice_recorder = None
		self.gpt_client = None
		self.whisper_client = None
		self.listener = None
		return


	def load_waifu(self):
		self.whisper_client = transcriber.whisper_client()
		self.whisper_client.load("base")

		self.gpt_client = chat.gpt_client()
		self.gpt_client.load_api_key(OPENAI_API_KEY_FILE)
		self.gpt_client.load_model_davinci()

		self.voice_recorder = recorder.audio_recorder(WAVE_OUTPUT_FILE)

	def run_chat_pipeline(self):
		prompt = ""
		try:
			prompt = self.whisper_client.transcribe(WAVE_OUTPUT_FILE)
			print("User: \"" + prompt + "\"")
		except err:
			print(err)
			return

		if prompt == "":
			return

		try:
			response = self.gpt_client.chat(prompt)
			print("wAIfu: \"" + response + "\"")
		except err:
			print(err)
			return

		# TODO integrate voice synthesis when added

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
