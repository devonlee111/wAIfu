import json
import openai

class gpt_client():
	def __init__(self):
		self.api_key = ""
		self.model = None
		self.prompt = ""
		self.temperature = 1.0
		self.freq_pen = 2.0
		self.pres_pen = 2.0
		return

	def load_api_key(self, key_file):
		key_file = open(key_file)
		key = key_file.read().strip()
		self.api_key = key
		openai.api_key = self.api_key
		return

	def load_model_gpt_3_5(self):
		self.model = "gpt-3.5-turbo"
		return

	def chat(self, messages):
		try:
			response = openai.Completion.create(
				model = self.model,
				messages = messages,
				temperature=self.temperature,
				frequency_penalty=self.freq_pen,
				presence_penaly=self.pres_pen,
				stop=["\n"]
			)
		except:
			raise

		return response['choices'][0]['message']['content'].strip()
