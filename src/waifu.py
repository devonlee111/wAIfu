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

		self.voice_recorder = recorder.audio_recorder(WAVE_OUTPUT_FILE)

	def run_chat_pipeline(self):
		prompt = ""
		try:
			prompt = self.whisper_client.transcribe(WAVE_OUTPUT_FILE)
		except err:
			print(err)
			return

		try:
			self.gpt_client.chat(prompt)
		except err:
			print (err)
			return

		# TODO integrate voice synthesis when added

	def on_press(self, key):
		if key.char == 'r':
			self.voice_recorder.start()
		return True

	def on_release(self, key):
		if key.char == 'r':
			self.voice_recorder.stop()
			self.run_chat_pipeline()
			return True
		# Any other key ends the program
		return False

	def run(self):
		print("Press and hold the 'r' key to begin recording")
		print("Release the 'r' key to end recording")
		self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
		self.listener.start()
		self.listener.join()

if __name__ == "__main__":
	waifu = waifu()
	waifu.load_waifu()
	waifu.run()
