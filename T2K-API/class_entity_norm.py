class entity_norm:
	utility = None

	# --

	def __init__(self):
		import class_utility

		self.utility = class_utility.utility()

	# --

	def norm_entity(self, cell_list):
		norm_dict = {}

		norm_list = []

		# --

		for surface in cell_list:
			# -- 데이터타입 개체 표면형 정규화

			if self.utility.is_literal(surface):
				norm = self.utility.norm_literal(surface, {'date': '0000-00-00'})

			# -- 오브젝트 개체 표면형 정규화

			else:
				norm = self.utility.norm_name(surface)

			# --

			norm_dict[surface] = norm

			norm_list.append(norm)

		# --

		norm_list = list(set(norm_list))

		# --

		return norm_dict, norm_list