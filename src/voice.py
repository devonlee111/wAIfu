from TTS.api import TTS

YOURTTS_MODEL = "tts_models/multilingual/multi-dataset/your_tts"

class coqui_voice_synthesizer():
	def __init__(self):
		self.tts = None
		self.model = None
		self.speaker = None
		self.language = None
		return

	def set_model(self, model, speaker = None, language = None):
		self.speaker = speaker
		self.language = language
		self.model = model
		return

	def load(self):
		self.tts = TTS(model_name=self.model)
		return

	def synthesize_speech(self, text, output_file, voice_to_clone = None):
		if self.tts == None:
			raise Exception("no model has been loaded")
			return

		if self.model != YOURTTS_MODEL:
			try:
				self.tts.tts_to_file(text, file_path=output_file)
			except Exception as e:
				raise e

		if self.tts.speakers != None and self.speaker == None:
			raise Exception(f"tts model { self.model } requires a speaker selection, but none was loaded")

		if self.tts.languages != None and self.language == None:
			raise Exception(f"tts model { self.model } requires a language selection, but none was loaded")

		# Perform speech synthesis with voice cloning
		# This only works for the yourTTS model
		if self.model == YOURTTS_MODEL and voice_to_clone != None:
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
