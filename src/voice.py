import requests
from TTS.api import TTS

CHUNK_SIZE = 1024
ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/"
YOURTTS_MODEL = "tts_models/multilingual/multi-dataset/your_tts"

class voice_synthesizer():
	def __init(self):
		return

	def synthesize_speech(self):
		return

class coqui_voice_synthesizer():
	def __init__(self, model = "", speaker = "", language = "", voice_to_clone = ""):
		self.tts = None
		self.model = model
		self.speaker = speaker
		self.language = language
		self.voice_to_clone = voice_to_clone
		return

	def set_model(self, model, speaker = "", language = ""):
		self.speaker = speaker
		self.language = language
		self.model = model
		return

	def load(self):
		self.tts = TTS(model_name=self.model)
		return

	def set_clone_voice_file(self, voice_to_clone):
		self.voice_to_clone = voice_to_clone
		return

	def synthesize_speech(self, text, output_file):
		if self.tts == None:
			raise Exception("no model has been loaded")
			return

		if self.model != YOURTTS_MODEL:
			try:
				self.tts.tts_to_file(text, file_path=output_file)
			except Exception as e:
				raise e

		if self.tts.speakers != None and self.speaker == "" and self.voice_to_clone == "":
			raise Exception(f"tts model { self.model } requires a speaker selection, but none was loaded")

		if self.tts.languages != None and self.language == "":
			raise Exception(f"tts model { self.model } requires a language selection, but none was loaded")

		# Perform speech synthesis with voice cloning
		# This only works for the yourTTS model
		if self.model == YOURTTS_MODEL and self.voice_to_clone != "":
			try:
				self.tts.tts_to_file(text, speaker_wav=voice_to_clone, language=self.language, file_path=output_file)
			except Exception as e:
				raise e
			return

		try:
			self.tts.tts_to_file(text, speaker=self.speaker, language=self.language, file_path=output_file)
		except Exception as e:
			raise e

		return

class eleven_labs_voice_synthesizer():
	def __init__(self, API_key = "", model_id = ""):
		self.API_key = API_key
		self.model_id = model_id
		return

	def set_model(self, model_id):
		self.model_id = model_id
		return

	def set_api_key(self, API_key):
		self.API_key = API_key
		return

	def synthesize_speech(self, text, output_file):
		if self.API_key == "":
			raise Exception(f"Eleven Labs API key required but not specified")

		if self.model_id == "":
			raise Exception(f"Eleven Labs Model ID required but not specified")

		headers = {
			"Accept": "audio/mpeg",
  			"Content-Type": "application/json",
			"xi-api-key": self.API_key
		}

		data = {
			"text": text,
  			"voice_settings": {
    			"stability": 0,
    			"similarity_boost": 0
			}
		}

		url = ELEVENLABS_TTS_URL + self.model_id

		response = requests.post(url, json=data, headers=headers)
		with open(output_file, 'wb') as f:
			for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
				if chunk:
					f.write(chunk)

		return
