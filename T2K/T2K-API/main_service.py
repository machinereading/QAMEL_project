# -*- coding: utf-8 -*-

def service(i_json):
	o_json = []

	# --

	html_table = i_json['html_table']

	# -- table parsing & exclusion

	import class_table_processing

	TP = class_table_processing.table_processing()

	table = TP.parse(html_table)

	if TP.is_rejected(table):
		return []

	print('table', table)

	# -- entity norm

	import class_entity_norm

	EN = class_entity_norm.entity_norm()

	# --

	cell_list = []

	table_head, table_body = table

	for row in table_body:
		for cell in row:
			cell_list.append(cell)

	# --

	norm_dict, norm_list = EN.norm_entity(cell_list)

	print('norm_dict', norm_dict)

	# -- entity linking

	import class_entity_linking

	EL = class_entity_linking.entity_linking()

	# --

	link_dict = EL.link_entity(norm_list, KB)

	print('link_dict', link_dict)

	# -- table to text

	import class_table_to_text

	TT = class_table_to_text.table_to_text()

	# --

	text_list = []

	text_list += TT.table_to_text(table, norm_dict, link_dict, KB)

	print('text_list', text_list)

	# -- predicate linking

	import class_utility

	utility = class_utility.utility()

	L2K_input = []

	for e1, e2, p0, e1_type, e2_type, p, text in text_list:
		sentence = text.replace(utility.uri2name(e1), ' << {0} >> '.format(utility.uri2name(e1)))
		sentence = sentence.replace(utility.uri2name(e2), ' << {0} >> '.format(utility.uri2name(e2)))

		L2K_input.append(sentence)

	# --

	import json

	L2K_response = POST_request('http://localhost:60005/service', json.dumps(L2K_input))
	
	L2K_output = []

	import json

	for four_tuple in json.loads(L2K_response):
		L2K_output.append(tuple(four_tuple))

	L2K_output = list(set(L2K_output))

	print('L2K_output', L2K_output)

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

	print('postprocessed_output', postprocessed_output)
	
	# -- domain/range filtering

	o_json = postprocessed_output
	
	'''
	for KB_s, KB_p, KB_o, c in postprocessed_output:
		if KB.check_domain_range(KB_s, KB_p, KB_o):
			o_json.append([KB_s, KB_p, KB_o, c])
	'''
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

with open('service-address.json') as i_file:
	import json

	service_info = json.loads(i_file.read())

# --

import class_KB

KB = class_KB.KB()

KB.load()

# --

from bottle import run

run(host=service_info['IP'], port=service_info['PORT'])