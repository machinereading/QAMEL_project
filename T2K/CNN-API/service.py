# -*- coding: utf-8 -*-

def service(i_json):
	o_json = []

	# --

	with open('data/test/ko_test.txt', 'w+') as o_file:
		for sentence in i_json:
			o_file.write(sentence + '\n')

	# --

	POST_request('http://localhost:60004/re-pcnn', '')

	# --
	'''
	import time

	time.sleep(0.5)
	'''
	# --

	with open('data/test/pl4-out-orig') as i_file:
		for line in i_file.readlines():
			line = line.strip()

			# --

			import re

			s_line = re.split('\t', line)

			# --

			s = s_line[0]
			p = s_line[1]
			o = s_line[2]
			c = s_line[4]

			# --

			o_json.append([s, p, o, c])

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

from bottle import run

run(host='localhost', port=60005)