import openai

class gpt_client():
	def __init__(self):
		self.api_key = ""
		self.model = None
		self.prompt = ""
		self.temperature = 0
		return

	def load_api_key(self, key_file):
		key_file = open(key_file)
		key = key_file.readlines()
		self.api_key = key
		openai.api_key = self.api_key
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
