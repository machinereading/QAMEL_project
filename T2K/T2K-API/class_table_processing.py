class table_processing:
	def parse(self, table_html):
		table_head = []

		table_body = []

		# --

		from bs4 import BeautifulSoup

		parsing = BeautifulSoup(table_html, 'html.parser')

		# --

		for x in parsing.find_all('tr'):
			if len(x.find_all('th')) > 0:
				head_row = []

				for y in x.find_all('th'):
					head_cell = str(y.text)

					head_cell = self.clean(head_cell)

					# --

					head_row.append(head_cell)

				# --

				if len(head_row) > 0:
					table_head.append(head_row)

			elif len(x.find_all('td')) > 0:
				body_row = []

				for y in x.find_all('td'):
					body_cell = str(y.text)

					body_cell = self.clean(body_cell)

					# --

					body_row.append(body_cell)

				# --

				if len(body_row) > 0:
					table_body.append(body_row)

		# --

		table_json = [table_head, table_body]

		return table_json

	def clean(self, cell):
		return cell
		
		cleaned = cell

		# -- 괄호 제거

		import re

		cleaned = re.sub(r'[({<\[].+[)}>\]]', '', cleaned)

		# -- 이스케이핑 문자 제거

		cleaned = re.sub(r'\\.', '', cleaned)

		# -- 연속된 공백 단일화

		cleaned = re.sub(r'\s+', ' ', cleaned)

		# -- 앞뒤 공백 제거

		cleaned = re.sub(r'\r\n', '', cleaned)

		cleaned = cleaned.strip()

		# --

		return cleaned

	def is_rejected(self, table_json):
		table_head, table_body = table_json

		# -- 헤드 로우가 없거나 여러 개일 경우

		if len(table_head) <= 0 or len(table_head) >= 2:
			return True

		# -- 바디 로우가 없을 경우

		if len(table_body) <= 0:
			return True

		# -- 헤드 로우와 모든 바디 로우가 같은 크기가 아닐 경우

		for row in table_body:
			if len(row) != len(table_head[0]):
				return True

		# --

		return False

	# --

	def dump_table_dict(self, table_dict):
		dump = '{\n'

		uri_list = sorted(table_dict.keys())

		for i in range(len(uri_list)):
			dump += ' ' * 4 + '"' + uri_list[i] + '":\n'

			if i < len(uri_list) - 1:
				dump += self.dump_list_3D(table_dict[uri_list[i]], 8) + ',\n'

			else:
				dump += self.dump_list_3D(table_dict[uri_list[i]], 8) + '\n'

		dump += '}'
		
		return dump

	def dump_list_3D(self, list_3D, indent):
		dump = ' ' * indent + '[\n'

		for i in range(len(list_3D)):
			list_2D = list_3D[i]

			# --

			dump += self.dump_list_2D(list_2D, indent+4)

			# --

			if i < len(list_3D) - 1:
				dump += ',\n'

			else:
				dump += '\n'

		dump += ' ' * indent + ']'

		return dump

	def dump_list_2D(self, list_2D, indent):
		dump = ' ' * indent + '[\n'

		for i in range(len(list_2D)):
			import json

			if i < len(list_2D) - 1:
				dump += ' ' * indent + ' ' * 4 + json.dumps(list_2D[i], ensure_ascii=False) + ',\n'

			else:
				dump += ' ' * indent + ' ' * 4 + json.dumps(list_2D[i], ensure_ascii=False) + '\n'

		dump += ' ' * indent + ']'

		return dump