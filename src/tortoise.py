# TODO
# Add integration with TorToiSe

class tortoise_client:
	def __init__(self):
		self.voice_model = ""
		self.preset = "fast"
		return

	def load_model(self, voice_model):
		self.voice_model = voice_model
		return

	def set_preset(self, preset):
		self.preset = preset
		return

	def speak(self, speech_file):
		# TODO finish integrating
		return
