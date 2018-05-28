class DS_data_extraction:
	utility = None

	# --

	def __init__(self):
		import class_utility

		self.utility = class_utility.utility()

	# --

	def placehold_sentence(self, norm_dict, link_dict):
		pholded_sentence_list = []

		# --

		for sentence in norm_dict.keys():
			surface_list = norm_dict[sentence].keys()

			# --

			linked_surface_list = list(surface_list)

			for surface in surface_list:
				if link_dict[norm_dict[sentence][surface]] == None:
					linked_surface_list.remove(surface)

			# --

			for e1 in linked_surface_list:
				for e2 in linked_surface_list:
					if e1 == e2:
						continue

					# --

					KB_e1 = link_dict[norm_dict[sentence][e1]]
					KB_e2 = link_dict[norm_dict[sentence][e2]]

					# --

					surface_idx_list = self.get_surface_idx_list(sentence, [e1, e2])

					# --

					for surface_1, begin_idx_1, end_idx_1 in surface_idx_list:
						for surface_2, begin_idx_2, end_idx_2 in surface_idx_list:
							if e1 != surface_1 or e2 != surface_2:
								continue

							# --

							pholded_sentence = str(sentence)

							# --

							# 시작이 같은 경우
							if begin_idx_1 == begin_idx_2 and end_idx_1 != end_idx_2:
								if end_idx_1 < end_idx_2:
									placeholder = surface_2.replace(self.get_head_noun(surface_1), ' << _sbj_ >> ').replace(self.get_head_noun(surface_2), ' << _obj_ >> ')

									pholded_sentence = pholded_sentence[0:begin_idx_2] + placeholder + pholded_sentence[end_idx_2:]

								elif end_idx_1 > end_idx_2:
									placeholder = surface_1.replace(self.get_head_noun(surface_2), ' << _obj_ >> ').replace(self.get_head_noun(surface_1), ' << _sbj_ >> ')

									pholded_sentence = pholded_sentence[0:begin_idx_1] + placeholder + pholded_sentence[end_idx_1:]

							# 끝이 같은 경우
							elif begin_idx_1 != begin_idx_2 and end_idx_1 == end_idx_2:
								if begin_idx_1 < begin_idx_2:
									placeholder = surface_1.replace(self.get_tail_noun(surface_2), ' << _obj_ >> ').replace(self.get_tail_noun(surface_1), ' << _sbj_ >> ')

									pholded_sentence = pholded_sentence[0:begin_idx_1] + placeholder + pholded_sentence[end_idx_1:]
									
								elif begin_idx_1 > begin_idx_2:
									placeholder = surface_2.replace(self.get_tail_noun(surface_1), ' << _sbj_ >> ').replace(self.get_tail_noun(surface_2), ' << _obj_ >> ')

									pholded_sentence = pholded_sentence[0:begin_idx_2] + placeholder + pholded_sentence[end_idx_2:]

							# S 가 O 를 포함하는 경우
							elif begin_idx_1 < begin_idx_2 and end_idx_1 > end_idx_2:
								placeholder = surface_1.replace(self.get_head_noun(surface_1), ' << _sbj_ >> ').replace(self.get_head_noun(surface_2), ' << _obj_ >> ')

								# --

								pholded_sentence = pholded_sentence[0:begin_idx_1] + placeholder + pholded_sentence[end_idx_1:]

							# O 가 S 를 포함하는 경우
							elif begin_idx_1 > begin_idx_2 and end_idx_1 < end_idx_2:
								placeholder = surface_2.replace(self.get_head_noun(surface_2), ' << _obj_ >> ').replace(self.get_head_noun(surface_1), ' << _sbj_ >> ')

								# --

								pholded_sentence = pholded_sentence[0:begin_idx_2] + placeholder + pholded_sentence[end_idx_2:]

							# 겹치지 않는 경우
							elif begin_idx_1 != begin_idx_2 and end_idx_1 != end_idx_2:
								placeholder_1 = ' << _sbj_ >> '
								placeholder_2 = ' << _obj_ >> '

								# --

								if end_idx_1 < end_idx_2:
									pholded_sentence = pholded_sentence[0:begin_idx_2] + placeholder_2 + pholded_sentence[end_idx_2:]
									pholded_sentence = pholded_sentence[0:begin_idx_1] + placeholder_1 + pholded_sentence[end_idx_1:]

								elif end_idx_1 > end_idx_2:
									pholded_sentence = pholded_sentence[0:begin_idx_1] + placeholder_1 + pholded_sentence[end_idx_1:]
									pholded_sentence = pholded_sentence[0:begin_idx_2] + placeholder_2 + pholded_sentence[end_idx_2:]

							# --

							if pholded_sentence.count(' << _sbj_ >> ') != 1:
								continue

							if pholded_sentence.count(' << _obj_ >> ') != 1:
								continue

							# --

							pholded_sentence_list.append([KB_e1, KB_e2, pholded_sentence])

		# --

		return pholded_sentence_list

	def extract_DS_sentence(self, pholded_sentence_list, KB):
		DS_sentences = []

		# --

		for e1, e2, pholded_sentence in pholded_sentence_list:
			try:
				for p in KB.enpair2property[e1][e2]:
					DS_sentences.append([self.utility.uri2name(e1), self.utility.uri2name(e2), self.utility.uri2name(p), pholded_sentence])

			except KeyError:
				pass

		# --

		return DS_sentences

	def get_embedding_sentence(self, DS_data):
		embedding_sentences = []

		# --

		for e1_name, e2_name, p, pholded_sentence in DS_data:
			embedding_sentence = pholded_sentence.replace(' << _sbj_ >> ', ' << {0} >> '.format(e1_name)).replace(' << _obj_ >> ', ' << {0} >> '.format(e2_name))

			embedding_sentences.append(embedding_sentence)

		# --

		return embedding_sentences

	def get_property_list(self, DS_data):
		p_list = []

		p_cnt = {}

		# --

		for s, o, p, pholded_sentence in DS_data:
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

	def get_surface_idx_list(self, sentence, surface_list):
		surface_idx_list = []

		for surface in surface_list:
			begin_idx = -1

			while True:
				try:
					begin_idx = sentence.index(surface, begin_idx+1)

				except ValueError:
					break

				end_idx = begin_idx + len(surface)

				surface_idx_list.append([surface, begin_idx, end_idx])

				# --

				try:
					sentence.index(surface, begin_idx+1)

				except ValueError:
					break

		surface_idx_list = sorted(surface_idx_list, key=lambda x: x[2], reverse=True)

		return surface_idx_list

	def get_head_noun(self, noun_phrase):
		if self.utility.is_literal(noun_phrase):
			return noun_phrase

		import re

		return re.split('\s+', noun_phrase)[-1]

	def get_tail_noun(self, noun_phrase):
		if self.utility.is_literal(noun_phrase):
			return noun_phrase

		import re

		return re.split('\s+', noun_phrase)[0]