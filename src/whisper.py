import whisper

EXCEPTION_NO_MODEL = "no model loaded"

class whisper_client():
	def __init__(self):
		self.model = None
		return

	def load(model_name):
		self.model = whisper.load_model(model_name)
		return

	def unload(model):
		del self.model
		return

	def transcribe(file):
		if MODEL == None:
			raise Exception(EXCEPTION_NO_MODEL)

		transcription = self.model.transcribe(file)
		return transcription["text"]
