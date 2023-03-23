import json
import openai

class gpt_client():
	def __init__(self):
		self.api_key = ""
		self.model = None
		self.prompt = ""
		self.temperature = 1
		return

	def load_api_key(self, key_file):
		key_file = open(key_file)
		key = key_file.read.strip()
		self.api_key = key
		openai.api_key = self.api_key
		return

	def load_model_davinci(self):
		self.model = "text-davinci-003"
		return

	def chat(self, prompt):
		try:
			response = openai.Completion.create(model=self.model, prompt=prompt, temperature=self.temperature)
		except:
			raise
		return response["choices"][0]["text"]
