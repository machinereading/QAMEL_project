def main():
	# --
	# entity detection
	# --

	try:
		with open('data/surface-dict.json') as i_file:
			import json

			surface_dict = json.loads(i_file.read())

	except FileNotFoundError:
		try:
			with open('data/NLP/NLP-news-list-pyeongchang-olympic.json') as i_file:
				import json

				parsing = json.loads(i_file.read())

		except FileNotFoundError:
			with open('data/news/news-list-pyeongchang-olympic.json') as i_file:
				import json

				news_list = json.loads(i_file.read())

			# --

			import class_NLP

			NLP = class_NLP.NLP()

			# --

			parsing = {}

			P = 0

			for url, title, date, content, provider in news_list:
				P += 1

				if P % 100 == 0:
					print('parsing', P, len(news_list))

				# --
				
				parsing[url] = NLP.parse(content)

			# --

			with open('data/NLP/NLP-news-list-pyeongchang-olympic.json', 'w+') as o_file:
				import json

				o_file.write(json.dumps(parsing, ensure_ascii=False))

		# --

		import class_entity_detection

		ED = class_entity_detection.entity_detection()

		# --

		surface_dict = {}

		P = 0

		for url in parsing.keys():
			P += 1

			if P % 1000 == 0:
				print('entity detection', P, len(parsing.keys()))

			# --

			surface_dict[url] = ED.detect_entity(parsing[url])

		# --

		with open('data/surface-dict.json', 'w+') as o_file:
			import json

			o_file.write(json.dumps(surface_dict, indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False))

	print('entity detected')

	# --

	url_set = set([])

	sentence_set = set([])

	for url in surface_dict.keys():
		url_set.add(url)

		for sentence in surface_dict[url].keys():
			sentence_set.add(sentence)

	print('url_set', len(url_set))
	
	print('sentence_set', len(sentence_set))

	# --
	# entity normalization
	# --

	with open('data/news/news-list-pyeongchang-olympic.json') as i_file:
		import json

		news_list = json.loads(i_file.read())

	try:
		with open('data/norm-dict.json') as i_file:
			import json

			norm_dict = json.loads(i_file.read())

		with open('data/norm-list.json') as i_file:
			import json

			norm_list = json.loads(i_file.read())

	except FileNotFoundError:
		import class_entity_norm

		EN = class_entity_norm.entity_norm()

		# --

		norm_dict = {}

		norm_list = []

		# --

		import class_utility

		utility = class_utility.utility()

		# --

		P = 0

		for url, title, date, content, provider in news_list:
			P += 1

			if P % 1000 == 0:
				print('entity normalization', P, len(news_list))

			# --

			norm_dict_url, norm_list_url = EN.norm_entity(surface_dict[url], {'date': utility.norm_article_date(date)})

			# --
			
			norm_dict[url] = norm_dict_url

			norm_list += norm_list_url

		# --

		norm_list = list(set(norm_list))

		# --

		with open('data/norm-dict.json', 'w+') as o_file:
			import json

			o_file.write(json.dumps(norm_dict, indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False))

		with open('data/norm-list.json', 'w+') as o_file:
			norm_list = list(norm_list)

			# --

			import json

			o_file.write(json.dumps(norm_list, indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False))

	print('entity normalized')

	# --
	# entity linking
	# --

	import class_KB

	KB = class_KB.KB()

	KB.load()

	print('KB loaded')

	# --

	try:
		with open('data/link-dict.json') as i_file:
			import json

			link_dict = json.loads(i_file.read())

	except FileNotFoundError:
		import class_entity_linking

		EL = class_entity_linking.entity_linking()

		# --

		import multiprocessing

		norm_queue = multiprocessing.Manager().Queue()

		for norm in norm_list:
			norm_queue.put(norm, False)

		# --

		link_dict = multiprocessing.Manager().dict()

		# --

		multiprocessing.Pool(12, EL.link_entity_multiprocess, (norm_queue, link_dict, KB))

		# --

		import time

		start_time = time.time()

		while not norm_queue.empty():
			print(['entity linking', len(norm_list) - norm_queue.qsize(), len(norm_list)])

			time.sleep(60)

		while len(link_dict.keys()) != len(norm_list):
			pass

		print(['entity linking', len(norm_list) - norm_queue.qsize(), len(norm_list)])

		print(['elapsed time', time.time() - start_time])

		# ==

		with open('data/link-dict.json', 'w+') as o_file:
			o_data = {}

			for norm in link_dict.keys():
				o_data[norm] = link_dict[norm]

			# --

			import json

			o_file.write(json.dumps(o_data, indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False))

	print('entity linked')

	# --
	# DS data extraction
	# --

	import class_DS_data_extraction

	DSDE = class_DS_data_extraction.DS_data_extraction()

	# --

	DS_data = []

	# --

	embedding_corpus = []

	# --

	P = 0

	for url in norm_dict.keys():
		P += 1

		if P % 1000 == 0:
			print('DS data extraction', P, len(norm_dict.keys()))

		# --

		pholded_sentence_list = DSDE.placehold_sentence(norm_dict[url], link_dict)

		# --

		DS_sentence_list = DSDE.extract_DS_sentence(pholded_sentence_list, KB)

		# --

		embedding_sentence_list = list(norm_dict[url].keys())

		embedding_sentence_list += DSDE.get_embedding_sentence(DS_sentence_list)

		# --

		DS_data += DS_sentence_list

		embedding_corpus += embedding_sentence_list

	# --

	p_list, p_cnt = DSDE.get_property_list(DS_data)

	# --

	with open('data/DS-data.tsv', 'w+') as o_file:
		for x in DS_data:
			o_file.write('\t'.join(x) + '\n')

	print('DS_data', len(DS_data))

	# --

	with open('data/DS-embedding-corpus.txt', 'w+') as o_file:
		for x in embedding_corpus:
			o_file.write(x + '\n')

	print('embedding_corpus', len(embedding_corpus))

	# --

	with open('data/DS-data-property-list.txt', 'w+') as o_file:
		trainable_p_list = []

		for p, cnt in sorted(p_cnt.items(), key=lambda x: x[1], reverse=True):
			if cnt >= 50:
				trainable_p_list.append(p)

		# --

		o_file.write(', '.join(trainable_p_list))

	print('trainable_p_list', len(trainable_p_list))

	# --

	with open('data/DS-data-property-count.tsv', 'w+') as o_file:
		for p, cnt in sorted(p_cnt.items(), key=lambda x: x[1], reverse=True):
			o_file.write('\t'.join([p, str(cnt)]) + '\n')

	# --

	for p, cnt in sorted(p_cnt.items(), key=lambda x: x[1], reverse=True):
		print(p, cnt)
	
# --

if __name__ == '__main__':
	main()