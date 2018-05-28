# -*- coding: utf-8 -*-

def service(i_json):
	o_json = []

	# --

	date = i_json['date']
	content = i_json['content']

	# -- parsing

	import class_NLP

	NLP = class_NLP.NLP()

	parsing = NLP.parse(content)

	# -- entity detection

	import class_entity_detection

	ED = class_entity_detection.entity_detection()

	surface_dict = ED.detect_entity(parsing)

	import json

	print('surface_dict', json.dumps(surface_dict, indent=4, separators=(',', ': '), ensure_ascii=False))

	# -- entity norm

	import class_entity_norm

	EN = class_entity_norm.entity_norm()

	import class_utility

	utility = class_utility.utility()

	norm_dict, norm_list = EN.norm_entity(surface_dict, {'date': utility.norm_article_date(date)})

	norm_list = list(set(norm_list))

	import json

	print('norm_dict', json.dumps(norm_dict, indent=4, separators=(',', ': '), ensure_ascii=False))

	print('norm_list', norm_list)

	# -- entity linking

	import class_entity_linking

	EL = class_entity_linking.entity_linking()

	link_dict = EL.link_entity(norm_list, KB)

	import json

	print('link_dict', json.dumps(link_dict, indent=4, separators=(',', ': '), ensure_ascii=False))

	# -- placeholded sentence extraction

	import class_DS_data_extraction

	DSDE = class_DS_data_extraction.DS_data_extraction()

	pholded_sentence_dict = {}

	for sentence in norm_dict.keys():
		pholded_sentence_dict = DSDE.placehold_sentence(norm_dict, link_dict)

	# -- predicate linking

	import class_utility

	utility = class_utility.utility()

	L2K_input = []

	for e1, e2, pholded_sentence in pholded_sentence_dict:
		sentence = pholded_sentence.replace(' << _sbj_ >> ', ' << {0} >> '.format(utility.uri2name(e1)))
		sentence = sentence.replace(' << _obj_ >> ', ' << {0} >> '.format(utility.uri2name(e2)))

		L2K_input.append(sentence)

	L2K_input = list(set(L2K_input))

	# --

	L2K_response = POST_request('http://qamel.kaist.ac.kr:60002/service', json.dumps(L2K_input))
	
	L2K_output = []

	import json

	for four_tuple in json.loads(L2K_response):
		L2K_output.append(tuple(four_tuple))

	L2K_output = list(set(L2K_output))

	#import json

	#print('L2K_output', json.dumps(L2K_output, indent=4, separators=(',', ': '), ensure_ascii=False))

	# -- post-processing

	postprocessed_output = []

	for s, p, o, c in L2K_output:
		entity_set = set([])

		for surface in link_dict.keys():
			if link_dict[surface] != None:
				if not utility.is_literal(link_dict[surface]):
					entity_set.add(link_dict[surface])

		# --

		if utility.is_literal(s):
			KB_s = s

		else:
			KB_s = utility.name2uri(s, entity_set)

		# --

		if utility.is_literal(o):
			KB_o = o

		else:
			KB_o = utility.name2uri(o, entity_set)

		# --

		KB_p = list(KB.p_name2uri[utility.uri2name(p)])[0]

		# --

		import re

		KB_p = re.sub(r'^dbo:', 'http://dbpedia.org/ontology/', KB_p)
		KB_p = re.sub(r'^dbp:', 'http://dbpedia.org/property/', KB_p)
		KB_p = re.sub(r'^sport:', 'http://www.bbc.co.uk/ontologies/sport/', KB_p)

		# --

		postprocessed_output.append([KB_s, KB_p, KB_o, c])

	import json

	print('postprocessed_output', json.dumps(postprocessed_output, indent=4, separators=(',', ': '), ensure_ascii=False))

	'''
	with open('postprocessed_output', 'w+') as o_file:
		import json

		o_file.write(json.dumps(postprocessed_output, indent=4, separators=(',', ': '), ensure_ascii=False))
	'''

	# -- domain/range filtering

	for KB_s, KB_p, KB_o, c in postprocessed_output:
		if KB.check_domain_range(KB_s, KB_p, KB_o):
			o_json.append([KB_s, KB_p, KB_o, c])

	# --

	return o_json

def POST_request(url, input_data):
	headers = {'Content-type': 'application/json'}

	# --

	import requests

	response = requests.post(url, data=input_data, headers=headers)

	return response.text

def enable_cors(fn):
	def _enable_cors(*args, **kwargs):
		from bottle import request, response

		# set CORS headers
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
		response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

		if request.method != 'OPTIONS':
			# actual request; reply with the actual response
			return fn(*args, **kwargs)
		
	return _enable_cors

from bottle import route

@route(path='/service', method=['OPTIONS', 'POST'])
@enable_cors
def do_service():
	from bottle import request

	i_text = request.body.read()

	# --

	import json

	try:
		i_json = json.loads(i_text)

	except TypeError:
		i_json = json.loads(i_text.decode('utf-8'))

	# --

	o_json = service(i_json)

	o_text = json.dumps(o_json, indent=4, separators=(',', ': '), ensure_ascii=False)	

	return o_text

# --

import class_KB

KB = class_KB.KB()

KB.load()

# --

with open('service-address.json') as i_file:
	import json

	service_info = json.loads(i_file.read())

# --

from bottle import run

run(host=service_info['IP'], port=service_info['PORT'])