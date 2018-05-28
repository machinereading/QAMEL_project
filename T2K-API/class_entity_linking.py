class entity_linking:
	utility = None

	# --

	def __init__(self):
		import class_utility

		self.utility = class_utility.utility()

	# --

	def link_entity(self, norm_list, KB):
		link_dict = {}

		# --

		prefix2name = {}

		for name in KB.name2entity.keys():
			try:
				prefix2name[name[0:4]].add(name)

			except KeyError:
				prefix2name[name[0:4]] = set([name])
		'''
		postfix2name = {}

		for name in KB.name2entity.keys():
			try:
				postfix2name[name[-2:]].add(name)

			except KeyError:
				postfix2name[name[-2:]] = set([name])
		'''
		# --

		for norm in norm_list:
			'''
			# [ EM-based linking ]

			if self.utility.is_literal(norm):
				link_dict[norm] = norm

			else:
				try:
					link_dict[norm] = self.most_frequent(KB.name2entity[norm], KB)

				except KeyError:
					link_dict[norm] = None
			'''
			
			# [ LS-based linking ]

			# -- 리터럴 개체 정규화

			if self.utility.is_literal(norm):
				link_dict[norm] = norm

			# -- 오브젝트 개체 링킹

			else:
				try:
					name_set = prefix2name[norm[0:4]]

				except KeyError:
					name_set = set([])
				'''
				try:
					name_set = name_set & postfix2name[norm[-2:]]

				except KeyError:
					name_set = set([])
				'''
				# --

				most_similar_name = None

				max_sim = -1.0

				for name in name_set:
					sim = self.levenshtein_similarity(name, norm)

					if sim > max_sim:
						most_similar_name = name

						max_sim = sim

				# --

				threshold = 0.7

				if max_sim >= threshold:
					link_dict[norm] = self.most_frequent(KB.name2entity[most_similar_name], KB)

				else:
					link_dict[norm] = None

		# --

		return link_dict

	def link_entity_multiprocess(self, norm_queue, link_dict, KB):
		prefix2name = {}

		for name in KB.name2entity.keys():
			try:
				prefix2name[name[0:4]].add(name)

			except KeyError:
				prefix2name[name[0:4]] = set([name])

		# --

		while not norm_queue.empty():
			try:
				norm = norm_queue.get(False)

			except:
				pass

			# --

			'''
			# [ EM-based linking ]

			if self.utility.is_literal(norm):
				link_dict[norm] = norm

			else:
				try:
					link_dict[norm] = self.most_frequent(KB.name2entity[norm], KB)

				except KeyError:
					link_dict[norm] = None
			'''

			# [ LS-based linking ]

			# -- 리터럴 개체 정규화

			if self.utility.is_literal(norm):
				link_dict[norm] = norm

			# -- 오브젝트 개체 링킹

			else:
				try:
					name_set = prefix2name[norm[0:4]]

				except KeyError:
					name_set = set([])

				# --

				most_similar_name = None

				max_sim = -1.0

				for name in name_set:
					sim = self.levenshtein_similarity(name, norm)

					if sim > max_sim:
						most_similar_name = name

						max_sim = sim

				# --

				threshold = 0.7

				if max_sim >= threshold:
					link_dict[norm] = self.most_frequent(KB.name2entity[most_similar_name], KB)

				else:
					link_dict[norm] = None

	# --

	def levenshtein_similarity(self, s, t):
		import editdistance

		distance = editdistance.eval(s, t)

		# --

		try:
			similarity = 1.0 - (float(distance) / float(max(len(s), len(t))))

		except ZeroDivisionError:
			similarity = 0.0

		# --

		return similarity

	# --

	def most_frequent(self, entity_list, KB):
		sorted_list = []

		# --

		for e1 in entity_list:
			sorted_list.append([e1, KB.entity2p_cnt[e1]])

		# --

		sorted_list = sorted(sorted_list, key=lambda x: x[1], reverse=True)

		# --

		most_frequent_entity = sorted_list[0][0]

		# --

		return most_frequent_entity