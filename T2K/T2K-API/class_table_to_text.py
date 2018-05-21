class table_to_text:
	utility = None

	# --

	def __init__(self):
		import class_utility

		self.utility = class_utility.utility()

	# --

	def table_to_text(self, table, norm_dict, link_dict, KB):
		table_head, table_body = table

		# --

		row_num = len(table_body)
		col_num = len(table_head[0])

		# --

		index_list = []

		# --

		p_cnt = {}

		e1_type_cnt = {}
		e2_type_cnt = {}

		# --

		for i in range(col_num):
			for j in range(col_num):
				if i == j:
					continue

				# --

				for k in range(row_num):
					e1 = link_dict[norm_dict[table_body[k][i]]]

					if e1 == None:
						continue

					# --

					e2 = link_dict[norm_dict[table_body[k][j]]]

					if e2 == None:
						continue

					# --

					try:
						KB.enpair2property[e1][e2]

					except KeyError:
						continue

					# --

					for p in KB.enpair2property[e1][e2]:
						try:
							p_cnt[(i, j)]

						except KeyError:
							p_cnt[(i, j)] = {}

						try:
							p_cnt[(i, j)][p] += 1

						except KeyError:
							p_cnt[(i, j)][p] = 1

					# --

					try:
						e1_type_cnt[(i, j)]

					except KeyError:
						e1_type_cnt[(i, j)] = {}

					# --

					e1_type_set = KB.get_specific_type(e1)

					if len(e1_type_set) > 0:
						for e1_type in e1_type_set:
							try:
								e1_type_cnt[(i, j)][e1_type] += 1

							except KeyError:
								e1_type_cnt[(i, j)][e1_type] = 1

					else:
						e1_type_cnt[(i, j)]['None'] = 1

					# --

					try:
						e2_type_cnt[(i, j)]

					except KeyError:
						e2_type_cnt[(i, j)] = {}

					# --

					e2_type_set = KB.get_specific_type(e2)

					if len(e2_type_set) > 0:
						for e2_type in e2_type_set:
							try:
								e2_type_cnt[(i, j)][e2_type] += 1

							except KeyError:
								e2_type_cnt[(i, j)][e2_type] = 1

					else:
						e2_type_cnt[(i, j)]['None'] = 1

					# --

					index_list.append((i, j))

		# --

		for i, j in p_cnt.keys():
			p_cnt[(i, j)] = sorted(p_cnt[(i, j)].items(), key=lambda x: x[1], reverse=True)

		for i, j in e1_type_cnt.keys():
			e1_type_cnt[(i, j)] = sorted(e1_type_cnt[(i, j)].items(), key=lambda x: x[1], reverse=True)

		for i, j in e2_type_cnt.keys():
			e2_type_cnt[(i, j)] = sorted(e2_type_cnt[(i, j)].items(), key=lambda x: x[1], reverse=True)

		# --

		index_list = list(set(index_list))

		# --

		text_list = []

		for i, j in index_list:
			for k in range(row_num):
				e1 = link_dict[norm_dict[table_body[k][i]]]

				if e1 == None:
					e1 = table_body[k][i]

				if len(e1) <= 0:
					continue

				# --

				e2 = link_dict[norm_dict[table_body[k][j]]]

				if e2 == None:
					e2 = table_body[k][j]

				if len(e2) <= 0:
					continue

				# --

				p0 = table_head[0][j]

				if len(p0) <= 0:
					continue

				# --

				e1_type = e1_type_cnt[(i, j)][0][0]

				# --

				e2_type = e2_type_cnt[(i, j)][0][0]

				# --

				p = p_cnt[(i, j)][0][0]

				# --
				'''
				if (ord(p0[-1]) - 44032) % 28 == 0:
					# 종성이 없는 경우
					text = '{0}의 {1}는 {2}이다.'.format(self.utility.uri2name(e1), p0, self.utility.uri2name(e2))

				else:
					# 종성이 있는 경우
					text = '{0}의 {1}은 {2}이다.'.format(self.utility.uri2name(e1), p0, self.utility.uri2name(e2))
				'''

				if (ord(p0[-1]) - 44032) % 28 == 0:
					# 종성이 없는 경우
					text = '{0} ({1})의 {2}는 {3} ({4})이다.'.format(self.utility.uri2name(e1), e1_type, p0, self.utility.uri2name(e2), e2_type)

				else:
					# 종성이 있는 경우
					text = '{0} ({1})의 {2}은 {3} ({4})이다.'.format(self.utility.uri2name(e1), e1_type, p0, self.utility.uri2name(e2), e2_type)
				
				# --

				text_list.append((e1, e2, p0, e1_type, e2_type, p, text))

		# --

		text_list = list(set(text_list))

		# --

		return text_list