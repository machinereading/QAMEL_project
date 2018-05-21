class NLP:
	def parse(self, text):
		return self.parse_konlpy(text)

		#return self.parse_ETRI(text)

	# --

	def parse_konlpy(self, text):
		from konlpy.tag import Kkma

		kkma = Kkma()

		# --

		from konlpy.tag import Twitter

		twitter = Twitter()

		# --

		sentence_list = kkma.sentences(text)

		# --

		parsing = []

		for sentence in sentence_list:
			parsed_sentence = {}

			# --

			parsed_sentence['text'] = sentence

			# --

			parsed_sentence['morp'] = kkma.pos(sentence)

			# --

			parsed_sentence['phrase'] = twitter.phrases(sentence)

			# --

			parsing.append(parsed_sentence)

		# --

		return parsing

	def parse_ETRI(self, text):
		input_data = {'sentence': text}

		# --

		try:
			import json

			return json.loads(self.POST_request('http://143.248.135.20:22334/controller/service/etri_parser', input_data))['sentence']

		except:
			return []

	def POST_request(self, url, input_data):
		headers = {'Content-type': 'application/x-www-form-urlencoded'}

		# --

		import requests

		response = requests.post(url, data=input_data, headers=headers)

		return response.text