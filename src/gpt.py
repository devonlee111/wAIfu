import openai

class gpt_client():
	def __init__(self, output_file):
		self.api_key = ""
		self.model = None
		self.prompt = ""
		self.temperature = 0
		return

	def load_api_key(key_file):
		key_file = open(key_file)
		key = key_file.readlines()
		openai.api_key = key
		return

	def load_model_davinci():
		model = "text-davinci-003"
		return

	def chat(prompt):
		try:
			response = openai.Completion.create(model=model, prompt=prompt, temperature=temperature)
		except:
			raise
		return response
