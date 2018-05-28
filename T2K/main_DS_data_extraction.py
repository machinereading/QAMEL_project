def main():
	# -- 테이블 파싱, 리젝션

	try:
		with open('data/table-dict.json') as i_file:
			import json

			table_dict = json.loads(i_file.read())

	except:
		with open('data/wikipedia/raw_tables_ko.ttl') as i_file:
			table_html = {}

			for line in i_file.readlines():
				line = line.strip()

				# --

				import re

				try:
					s, p, o = re.findall(r'^<(.+)> <(.+)> <(.+)> \.$', line)[0]
					
				except:
					try:
						s, p, o = re.findall(r'^<(.+)> <(.+)> "(.+)"(?:\^\^<.+>)? \.$', line)[0]

					except:
						continue

				# --

				if p == 'http://purl.org/dc/elements/1.1/source':
					table_html[s] = o

		print('table_html', len(table_html.keys()))

		# --

		import class_table_processing

		TP = class_table_processing.table_processing()

		# --

		table_dict = {}

		table_dict_reject = {}

		P = 0

		for uri in table_html.keys():
			P += 1

			if P % 1000 == 0:
				print(P, len(table_html.keys()))

			# --

			table_head, table_body = TP.parse(table_html[uri])

			# --

			table = [table_head, table_body]

			# --

			if not TP.is_rejected(table):
				table_dict[uri] = table

			else:
				table_dict_reject[uri] = table

		print('table_dict', len(table_dict.keys()))

		# --

		with open('data/table-dict.json', 'w+') as o_file:
			import json

			o_file.write(TP.dump_table_dict(table_dict))

		with open('data/table-dict-reject.json', 'w+') as o_file:
			import json

			o_file.write(TP.dump_table_dict(table_dict_reject))

	print('table parsed, rejected')

	# -- 개체 정규화

	try:
		with open('data/norm-dict.json') as i_file:
			import json

			norm_dict = json.loads(i_file.read())

		with open('data/norm-list.json') as i_file:
			import json

			norm_list = json.loads(i_file.read())

	except:
		import class_entity_norm

		EN = class_entity_norm.entity_norm()

		# --

		cell_list = []

		for uri in table_dict.keys():
			table_head, table_body = table_dict[uri]

			for row in table_body:
				for cell in row:
					cell_list.append(cell)

		# --

		norm_dict, norm_list = EN.norm_entity(cell_list)

		# --

		with open('data/norm-dict.json', 'w+') as o_file:
			import json

			o_file.write(json.dumps(norm_dict, indent=4, separators=(',', ': '), ensure_ascii=False))

		with open('data/norm-list.json', 'w+') as o_file:
			import json

			o_file.write(json.dumps(norm_list, indent=4, separators=(',', ': '), ensure_ascii=False))

	print('entity normed')

	# -- KB 로드

	import class_KB

	KB = class_KB.KB()

	KB.load()

	print('KB loaded')

	# -- 개체 링킹

	try:
		with open('data/link-dict.json') as i_file:
			import json

			link_dict = json.loads(i_file.read())

	except:
		import class_entity_linking

		EL = class_entity_linking.entity_linking()

		# --

		link_dict = EL.link_entity(norm_list, KB)

		# --

		with open('data/link-dict.json', 'w+') as o_file:
			import json

			o_file.write(json.dumps(link_dict, indent=4, separators=(',', ': '), ensure_ascii=False))

	print('entity linked')

	# -- 테이블 투 텍스트

	text_list = []

	text_dict = {}

	try:
		with open('data/text-list.json') as i_file:
			import json

			text_list = json.loads(i_file.read())

	except:
		import class_table_to_text

		TT = class_table_to_text.table_to_text()

		# --

		text_list = []

		for uri in table_dict.keys():
			table = table_dict[uri]

			# --

			text_list += TT.table_to_text(table, norm_dict, link_dict, KB)

			# --

			text_dict[uri] = TT.table_to_text(table, norm_dict, link_dict, KB)

		# --

		with open('data/text-list.json', 'w+') as o_file:
			import json

			o_file.write(json.dumps(text_list, indent=4, separators=(',', ': '), ensure_ascii=False))

		with open('data/text-dict.json', 'w+') as o_file:
			import json

			o_file.write(json.dumps(text_dict, indent=4, separators=(',', ': '), ensure_ascii=False))

		# --

		p0_cnt = {}

		for uri in text_dict.keys():
			p0_set = set([])

			# --

			for e1, e2, p0, e1_type, e2_type, p, text in text_dict[uri]:
				p0_set.add(p0)

			# --

			p0_cnt[uri] = len(p0_set)

		# --

		with open('data/p0-cnt.tsv', 'w+') as o_file:
			for uri, cnt in sorted(p0_cnt.items(), key=lambda x: x[1], reverse=True):
				o_file.write('\t'.join([uri, str(cnt)]) + '\n')


	print('text extracted')

	# -- DS 데이터 추출

	import class_DS_data_extraction

	DSDE = class_DS_data_extraction.DS_data_extraction()

	# --

	DS_data = DSDE.extract_DS_data(text_list, KB)

	embedding_corpus = DSDE.extract_embedding_corpus(DS_data)

	p_list, p_cnt = DSDE.extract_property_list(DS_data)

	# --

	with open('data/DS-data.tsv', 'w+') as o_file:
		for e1, e2, p, pholded_sentence in DS_data:
			o_file.write('\t'.join([e1, e2, p, pholded_sentence]) + '\n')

	print('DS_data', len(DS_data))

	# --

	with open('data/DS-embedding-corpus.txt', 'w+') as o_file:
		for sentence in embedding_corpus:
			o_file.write(sentence + '\n')

	print('embedding_corpus', len(embedding_corpus))

	# --

	with open('data/DS-data-property-list.txt', 'w+') as o_file:
		trainable_p_list = []

		for p, cnt in sorted(p_cnt.items(), key=lambda x: x[1], reverse=True):
			if cnt >= 10:
				trainable_p_list.append(p)

		# --

		o_file.write(', '.join(trainable_p_list))

	print('trainable_p_list', len(trainable_p_list))

	# --

	with open('data/DS-data-property-count.tsv', 'w+') as o_file:
		for p, cnt in sorted(p_cnt.items(), key=lambda x: x[1], reverse=True):
			o_file.write('\t'.join([p, str(cnt)]) + '\n')

	for p, cnt in sorted(p_cnt.items(), key=lambda x: x[1], reverse=True):
		print(p, cnt)

# --

if __name__ == '__main__':
	main()