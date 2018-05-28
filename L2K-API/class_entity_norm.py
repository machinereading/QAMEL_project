class entity_norm:
	utility = None

	# --

	def __init__(self):
		import class_utility

		self.utility = class_utility.utility()

	# --

	def norm_entity(self, surface_dict, article_info):
		norm_dict = {}

		norm_list = []

		# --

		for sentence in surface_dict.keys():
			norm_dict[sentence] = {}

			# --

			for surface in surface_dict[sentence]:
				# -- 데이터타입 개체 표면형 정규화

				if self.utility.is_literal(surface):
					norm = self.utility.norm_literal(surface, article_info)

				# -- 오브젝트 개체 표면형 정규화

				else:
					norm = self.utility.norm_name(surface)

				# --

				norm_dict[sentence][surface] = norm

				norm_list.append(norm)

		# --

		norm_list = list(set(norm_list))

		# --

		return norm_dict, norm_list