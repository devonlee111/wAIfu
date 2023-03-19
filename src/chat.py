import openai

class gpt_client():
	def __init__(self, output_file):
		self.api_key = ""
		self.model = None
		self.prompt = ""
		self.temperature = 0
		return

	def load_api_key(self, key_file):
		self.key_file = open(key_file)
		self.key = key_file.readlines()
		self.openai.api_key = key
		return

	def load_model_davinci(self):
		self.model = "text-davinci-003"
		return

	def chat(self, prompt):
		try:
			response = openai.Completion.create(model=model, prompt=prompt, temperature=temperature)
		except:
			raise
		return response
