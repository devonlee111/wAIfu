import openai
import whisper

EXCEPTION_NO_MODEL = "no model loaded"

class whisper_client():
	def __init__(self):
		self.language = "en"
		self.api_key = ""
		self.use_local_engine = False
		self.model = None
		return

	def set_api_key(self, api_key):
		self.api_key = api_key
		return

	def use_local(self):
		self.use_local_engine = True
		return

	def use_API(self):
		self.use_local_engine = False
		return

	def load(self, model_name, language):
		self.language = language
		self.model = whisper.load_model(model_name)
		return

	def unload(self, model):
		del self.model
		return

	def transcribe(self, file):
		transcription = ""
		if self.use_local_engine:
			if self.model == None:
				raise Exception(EXCEPTION_NO_MODEL)

			transcription = self.model.transcribe(file)
		else:
			audio_file = open("file", self.language)
			transcription = openai.Audio.transcribe("whisper-1", audio_file)

		return transcription["text"]
