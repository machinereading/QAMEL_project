class DS_data_extraction:
	utility = None

	# --

	def __init__(self):
		import class_utility

		self.utility = class_utility.utility()

	# --

	def extract_DS_data(self, text_list, KB):
		DS_data = []

		# --

		for e1, e2, p0, e1_type, e2_type, p, text in text_list:
			pholded_sentence = text.replace(self.utility.uri2name(e1), ' << _sbj_ >> ', 1).replace(self.utility.uri2name(e2), ' << _obj_ >> ', 1)

			DS_data.append((self.utility.uri2name(e1), self.utility.uri2name(e2), self.utility.uri2name(p), pholded_sentence))
			
			'''
			try:
				for p in KB.enpair2property[e1][e2]:
					pholded_sentence = text.replace(self.utility.uri2name(e1), ' << _sbj_ >> ', 1).replace(self.utility.uri2name(e2), ' << _obj_ >> ', 1)

					DS_data.append((self.utility.uri2name(e1), self.utility.uri2name(e2), self.utility.uri2name(p), pholded_sentence))

			except KeyError:
				pass
			'''

		# --

		DS_data = list(set(DS_data))

		# --

		return DS_data

	# --

	def extract_embedding_corpus(self, DS_data):
		embedding_corpus = []

		# --

		for e1, e2, p, pholded_sentence in DS_data:
			sentence = pholded_sentence.replace(' << _sbj_ >> ', ' << ' + e1 + ' >> ').replace(' << _obj_ >> ', ' << ' + e2 + ' >> ')

			embedding_corpus.append(sentence)

		# --

		embedding_corpus = list(set(embedding_corpus))

		# --

		return embedding_corpus

	def extract_property_list(self, DS_data):
		p_list = []

		p_cnt = {}

		# --

		for e1, e2, p, pholded_sentence in DS_data:
			p_list.append(p)

			# --

			try:
				p_cnt[p] += 1

			except KeyError:
				p_cnt[p] = 1

		# --

		p_list = sorted(set(p_list))

		# --

		return p_list, p_cnt

	def archive(self):
		# -- 180419

		try:
			for p in KB.enpair2property[e1][e2]:
				pholded_sentence = text.replace(self.utility.uri2name(e1), ' << _sbj_ >> ', 1).replace(self.utility.uri2name(e2), ' << _obj_ >> ', 1)

				DS_data.append((self.utility.uri2name(e1), self.utility.uri2name(e2), self.utility.uri2name(p), pholded_sentence))

				
				'''
				pholded_sentence = ' << _sbj_ >>  {0}  << _obj_ >> .'.format(p0)

				DS_data.append((self.utility.uri2name(e1), self.utility.uri2name(e2), self.utility.uri2name(p), pholded_sentence))
				'''
				'''
				try:
					e1_types = KB.entity2type[e1]

				except KeyError:
					continue

				try:
					e2_types = KB.entity2type[e2]

				except KeyError:
					continue

				for e1_type in e1_types:
					for e2_type in e2_types:
						pholded_sentence = ' << _sbj_ >> ({0})의 {1}는  << _obj_ >> ({2})이다.'.format(e1_type, p0, e2_type)

						DS_data.append((self.utility.uri2name(e1), self.utility.uri2name(e2), self.utility.uri2name(p), pholded_sentence))
				'''
		except KeyError:
			pass