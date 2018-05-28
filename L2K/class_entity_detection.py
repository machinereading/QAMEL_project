class entity_detection:
	def detect_entity(self, parsing):
		return self.detect_entity_konlpy(parsing)

		#return self.detect_entity_ETRI(parsing)

	# --

	def detect_entity_konlpy(self, parsing):
		tag_set = set(['NNG', 'NNP', 'NNB', 'NNM', 'NR', 'NP', 'XPN', 'XSN', 'OH', 'OL', 'ON'])

		# --

		surface_dict = {}

		# -- longest noun phrase

		for parsed_sentence in parsing:
			sentence = parsed_sentence['text']

			# -- 

			longest_NP_list = []

			longest_NP = []

			for morp_lemma, morp_type in parsed_sentence['morp']:
				if morp_type in tag_set:
					longest_NP.append(morp_lemma)

				else:
					if len(longest_NP) > 0:
						try:
							import re

							longest_NP = re.findall(r'(' + r'\s*'.join(longest_NP) + r')', sentence)[0].strip()

							longest_NP_list.append(longest_NP)

						except:
							pass

					# --
					
					longest_NP = []

			# --

			surface_dict[sentence] = list(set(longest_NP_list))
		
		# -- phrase

		for parsed_sentence in parsing:
			sentence = parsed_sentence['text']

			# --
			
			phrase_list = parsed_sentence['phrase']

			# --

			surface_dict[sentence] = list(set(surface_dict[sentence] + phrase_list))

		# --

		return surface_dict

	def detect_entity_ETRI(self, parsing):
		tag_set_1 = set(['NNP', 'SL', 'SH', 'SN'])
		tag_set_2 = set(['NNG', 'NNB', 'NR', 'NP', 'XPN', 'XSN'])

		# --

		surface_dict = {}

		# --

		if parsing == None:
			return surface_dict

		if len(parsing) <= 0:
			return surface_dict

		# -- longest noun phrase

		for parsed_sentence in parsing:
			sentence = parsed_sentence['text']

			# --

			sentence_length = len(parsed_sentence['morp'])

			# -- 

			longest_NP_list = []

			longest_NP = ''

			for i in range(len(parsed_sentence['morp'])):
				morp = parsed_sentence['morp'][i]

				# --

				try:
					next_morp = parsed_sentence['morp'][i+1]

				except:
					next_morp = parsed_sentence['morp'][i]

				# --

				if morp['type'] in tag_set_1 | tag_set_2:
					# -- 형태소 추가

					longest_NP += morp['lemma']
					
					# -- 공백 추가

					diff = next_morp['position'] - morp['position']

					space_num = diff - len(morp['lemma'].encode('utf-8'))

					for i in range(space_num):
						longest_NP += ' '

				else:
					if len(longest_NP) > 0:
						longest_NP = longest_NP.strip()

						# --

						longest_NP_list.append(longest_NP)

					# --
					
					longest_NP = ''

			# --

			if sentence_length <= 120:
				surface_dict[sentence] = list(set(longest_NP_list))

			else:
				pass
		
		# -- NE

		for parsed_sentence in parsing:
			sentence = parsed_sentence['text']

			# --

			sentence_length = len(parsed_sentence['morp'])

			# --
			
			NE_list = []

			for NE in parsed_sentence['NE']:
				NE_list.append(NE['text'])

			# --

			if sentence_length <= 120:
				surface_dict[sentence] = list(set(surface_dict[sentence] + NE_list))

			else:
				pass

		# --

		return surface_dict