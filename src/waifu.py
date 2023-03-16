from pynput import keyboard

import gpt
import recorder
import whisper

OPENAI_API_KEY_FILE = "./openai_key"
WAVE_OUTPUT_FILE = "output.wav"

voice_recorder = None
gpt_client = None
whisper_client = None

def load_waifu():
	whisper_client = whisper.whisper_client()
	whisper_client.load("base")

	gpt_client = gpt.gpt_client()
	gpt.load_api_key(OPENAI_API_KEY_FILE)

	voice_recorder = recorder.recorder(WAVE_OUTPUT_FILE)

def run_chat_pipeline():
	prompt = ""
	try:
		prompt = whisper_client.transcribe(WAVE_OUTPUT_FILE)
	except err:
		print(err)
		return

	try:
		gpt_client.chat(prompt)
	except err:
		print (err)
		return

	# TODO integrate voice synthesis when added

def run():
	print("Press and hold the 'r' key to begin recording")
	print("Release the 'r' key to end recording")
	listener = keyboard.Listener(on_press=on_press, on_release=on_release)
	listener.join()

def on_press(self, key):
	if key.char == 'r':
		voice_recorder.start()
	return True

def on_release(self, key):
	if key.char == 'r':
		voice_recorder.stop()
		run_chat_pipeline()
		return True
	# Any other key ends the program
	return False

if __name__ == "__main__":
	load_waifu()
	run()
