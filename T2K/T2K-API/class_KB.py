class KB:
	utility = None

	# -- schema

	subclass2superclass = {}

	p_name2type = {}
	p_name2domain = {}
	p_name2range = {}
	p_name2uri = {}

	# -- assertion

	entity_list = []
	literal_list = []

	entity2name = {}
	entity2type = {}

	name2entity = {}

	enpair2property = {}
	entity2p_cnt = {}

	# --

	def __init__(self):
		import class_utility

		self.utility = class_utility.utility()

	# --

	def load(self):
		self.load_schema()
		self.load_assertion()

		# --

		self.complete_type()

		# --

		self.count_property()

	# --

	def load_schema(self):
		with open('data/KB/user-schema.json') as i_file:
			import json

			for p, p_types, domains, ranges in json.loads(i_file.read()):
				for p_type in p_types:
					p_type = self.utility.norm_name(self.utility.uri2name(p_type))

					try:
						self.p_name2type[self.utility.uri2name(p)].add(p_type)

					except KeyError:
						self.p_name2type[self.utility.uri2name(p)] = set([p_type])

				# --

				for domain in domains:
					domain = self.utility.norm_name(self.utility.uri2name(domain))

					try:
						self.p_name2domain[self.utility.uri2name(p)].add(domain)

					except KeyError:
						self.p_name2domain[self.utility.uri2name(p)] = set([domain])

				# --

				for range_ in ranges:
					range_ = self.utility.norm_name(self.utility.uri2name(range_))

					try:
						self.p_name2range[self.utility.uri2name(p)].add(range_)

					except KeyError:
						self.p_name2range[self.utility.uri2name(p)] = set([range_])

		# --

		with open('data/KB/dbpedia_2016-10.nt') as i_file:
			for line in i_file.readlines():
				line = line.strip()

				# --

				import re

				match = re.findall(r'^<(.+)> <(.+)> <(.+)> \.$', line)

				if len(match) > 0:
					s = match[0][0]
					p = match[0][1]
					o = match[0][2]

					# --

					if p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
						p_types = ['http://www.w3.org/2002/07/owl#ObjectProperty', 'http://www.w3.org/2002/07/owl#DatatypeProperty', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property']

						if o in p_types:
							try:
								self.p_name2type[self.utility.uri2name(s)].add(self.utility.norm_name(self.utility.uri2name(o)))

							except KeyError:
								self.p_name2type[self.utility.uri2name(s)] = set([self.utility.norm_name(self.utility.uri2name(o))])

							try:
								self.p_name2uri[self.utility.uri2name(s)].add(s)

							except KeyError:
								self.p_name2uri[self.utility.uri2name(s)] = set([s])

					elif p == 'http://www.w3.org/2000/01/rdf-schema#domain':
						try:
							self.p_name2domain[self.utility.uri2name(s)].add(self.utility.norm_name(self.utility.uri2name(o)))

						except KeyError:
							self.p_name2domain[self.utility.uri2name(s)] = set([self.utility.norm_name(self.utility.uri2name(o))])

						try:
							self.p_name2uri[self.utility.uri2name(s)].add(s)

						except KeyError:
							self.p_name2uri[self.utility.uri2name(s)] = set([s])

					elif p == 'http://www.w3.org/2000/01/rdf-schema#range':
						try:
							self.p_name2range[self.utility.uri2name(s)].add(self.utility.norm_name(self.utility.uri2name(o)))

						except KeyError:
							self.p_name2range[self.utility.uri2name(s)] = set([self.utility.norm_name(self.utility.uri2name(o))])

						try:
							self.p_name2uri[self.utility.uri2name(s)].add(s)

						except KeyError:
							self.p_name2uri[self.utility.uri2name(s)] = set([s])

					elif p == 'http://www.w3.org/2000/01/rdf-schema#subClassOf':
						self.subclass2superclass[self.utility.norm_name(self.utility.uri2name(s))] = self.utility.norm_name(self.utility.uri2name(o))

	def load_assertion(self):
		redirect = {}

		with open('data/KB/redirects_ko.ttl') as i_file:
			for line in i_file.readlines():
				line = line.strip()

				# --

				if line[0] == '#':
					continue

				# --

				import re

				s, p, o = re.findall(r'^<(.+)> <(.+)> <(.+)> \.$', line)[0]

				# --

				redirect[s] = o

		# --

		with open('data/KB/olympic-triples-pyeongchang.json') as i_file:
			import json

			for s, p, o in json.loads(i_file.read()):
				self.entity_list.append(s)

				# --

				try:
					self.entity2name[s].add(self.utility.norm_name(self.utility.uri2name(s)))

				except KeyError:
					self.entity2name[s] = set([self.utility.norm_name(self.utility.uri2name(s))])

				# --

				if p == 'rdf:type':
					try:
						self.entity2type[s].add(self.utility.norm_name(self.utility.uri2name(o)))

					except KeyError:
						self.entity2type[s] = set([self.utility.norm_name(self.utility.uri2name(o))])

				else:
					if self.utility.is_literal(o):
						self.literal_list.append(o)

					else:
						self.entity_list.append(o)

						# --

						try:
							self.entity2name[o].add(self.utility.norm_name(self.utility.uri2name(o)))

						except KeyError:
							self.entity2name[o] = set([self.utility.norm_name(self.utility.uri2name(o))])

					# --

					try:
						self.enpair2property[s]

					except KeyError:
						self.enpair2property[s] = {}

					try:
						self.enpair2property[s][o].add(p)

					except KeyError:
						self.enpair2property[s][o] = set([p])

					# --

					try:
						self.p_name2uri[self.utility.uri2name(p)].add(p)

					except KeyError:
						self.p_name2uri[self.utility.uri2name(p)] = set([p])

		# --

		with open('data/KB/olympic-triples-sochi.json') as i_file:
			import json

			for s, p, o in json.loads(i_file.read()):
				self.entity_list.append(s)

				# --

				try:
					self.entity2name[s].add(self.utility.norm_name(self.utility.uri2name(s)))

				except KeyError:
					self.entity2name[s] = set([self.utility.norm_name(self.utility.uri2name(s))])

				# --

				if p == 'rdf:type':
					try:
						self.entity2type[s].add(self.utility.norm_name(self.utility.uri2name(o)))

					except KeyError:
						self.entity2type[s] = set([self.utility.norm_name(self.utility.uri2name(o))])

				else:
					if self.utility.is_literal(o):
						self.literal_list.append(o)

					else:
						self.entity_list.append(o)

						# --

						try:
							self.entity2name[o].add(self.utility.norm_name(self.utility.uri2name(o)))

						except KeyError:
							self.entity2name[o] = set([self.utility.norm_name(self.utility.uri2name(o))])

					# --

					try:
						self.enpair2property[s]

					except KeyError:
						self.enpair2property[s] = {}

					try:
						self.enpair2property[s][o].add(p)

					except KeyError:
						self.enpair2property[s][o] = set([p])

					# --

					try:
						self.p_name2uri[self.utility.uri2name(p)].add(p)

					except KeyError:
						self.p_name2uri[self.utility.uri2name(p)] = set([p])

		# --

		with open('data/KB/labels_ko.ttl') as i_file:
			for line in i_file.readlines():
				line = line.strip()

				# --

				if line[0] == '#':
					continue

				# --

				import re

				try:
					s, p, o, o_type = re.findall(r'^<(.+)> <(.+)> "(.+)"\^\^<(.+)> \.$', line)[0]

				except:
					o_type = None

					try:
						s, p, o = re.findall(r'^<(.+)> <(.+)> "(.+)"@.+ \.$', line)[0]

					except:
						s, p, o = re.findall(r'^<(.+)> <(.+)> "(.+)" \.$', line)[0]

				# --

				try:
					redirect[s]

					try:
						self.entity2name[redirect[s]].add(self.utility.norm_name(self.utility.uri2name(s)))

					except KeyError:
						self.entity2name[redirect[s]] = set([self.utility.norm_name(self.utility.uri2name(s))])

					s = redirect[s]

				except:
					pass

				# --
				
				self.entity_list.append(s)

				# --

				try:
					self.entity2name[s].add(self.utility.norm_name(self.utility.uri2name(s)))

				except KeyError:
					self.entity2name[s] = set([self.utility.norm_name(self.utility.uri2name(s))])

				# --

				if p == 'http://www.w3.org/2000/01/rdf-schema#label':
					try:
						self.entity2name[s].add(self.utility.norm_name(o))

					except KeyError:
						self.entity2name[s] = set([self.utility.norm_name(o)])

		# --

		with open('data/KB/instance_types_ko.ttl') as i_file:
			for line in i_file.readlines():
				line = line.strip()

				# --

				if line[0] == '#':
					continue

				# --

				import re

				s, p, o = re.findall(r'^<(.+)> <(.+)> <(.+)> \.$', line)[0]

				# --

				try:
					redirect[s]

					try:
						self.entity2name[redirect[s]].add(self.utility.norm_name(self.utility.uri2name(s)))

					except KeyError:
						self.entity2name[redirect[s]] = set([self.utility.norm_name(self.utility.uri2name(s))])

					s = redirect[s]

				except:
					pass

				# --

				self.entity_list.append(s)

				# --

				try:
					self.entity2name[s].add(self.utility.norm_name(self.utility.uri2name(s)))

				except KeyError:
					self.entity2name[s] = set([self.utility.norm_name(self.utility.uri2name(s))])

				# --

				try:
					self.entity2type[s].add(self.utility.norm_name(self.utility.uri2name(o)))

				except KeyError:
					self.entity2type[s] = set([self.utility.norm_name(self.utility.uri2name(o))])

		# --

		with open('data/KB/mappingbased_objects_ko.ttl') as i_file:
			for line in i_file.readlines():
				line = line.strip()

				# --

				if line[0] == '#':
					continue

				# --

				import re

				s, p, o = re.findall(r'^<(.+)> <(.+)> <(.+)> \.$', line)[0]

				# --

				try:
					redirect[s]

					try:
						self.entity2name[redirect[s]].add(self.utility.norm_name(self.utility.uri2name(s)))

					except KeyError:
						self.entity2name[redirect[s]] = set([self.utility.norm_name(self.utility.uri2name(s))])

					s = redirect[s]

				except:
					pass

				# --

				self.entity_list.append(s)

				# --

				try:
					self.entity2name[s].add(self.utility.norm_name(self.utility.uri2name(s)))

				except KeyError:
					self.entity2name[s] = set([self.utility.norm_name(self.utility.uri2name(s))])

				# --

				try:
					redirect[o]

					try:
						self.entity2name[redirect[o]].add(self.utility.norm_name(self.utility.uri2name(o)))

					except KeyError:
						self.entity2name[redirect[o]] = set([self.utility.norm_name(self.utility.uri2name(o))])

					o = redirect[o]

				except:
					pass

				# --

				self.entity_list.append(o)

				# --

				try:
					self.entity2name[o].add(self.utility.norm_name(self.utility.uri2name(o)))

				except KeyError:
					self.entity2name[o] = set([self.utility.norm_name(self.utility.uri2name(o))])

				# --

				try:
					self.enpair2property[s]

				except KeyError:
					self.enpair2property[s] = {}

				try:
					self.enpair2property[s][o].add(p)

				except KeyError:
					self.enpair2property[s][o] = set([p])

				# --

				try:
					self.p_name2uri[self.utility.uri2name(p)].add(p)

				except KeyError:
					self.p_name2uri[self.utility.uri2name(p)] = set([p])

		# --

		with open('data/KB/mappingbased_literals_ko.ttl') as i_file:
			for line in i_file.readlines():
				line = line.strip()

				# --

				if line[0] == '#':
					continue

				# --

				import re

				try:
					s, p, o, o_type = re.findall(r'^<(.+)> <(.+)> "(.+)"\^\^<(.+)> \.$', line)[0]

				except:
					o_type = None

					try:
						s, p, o = re.findall(r'^<(.+)> <(.+)> "(.+)"@.+ \.$', line)[0]

					except:
						s, p, o = re.findall(r'^<(.+)> <(.+)> "(.+)" \.$', line)[0]

				# --

				try:
					redirect[s]

					try:
						self.entity2name[redirect[s]].add(self.utility.norm_name(self.utility.uri2name(s)))

					except KeyError:
						self.entity2name[redirect[s]] = set([self.utility.norm_name(self.utility.uri2name(s))])

					s = redirect[s]

				except:
					pass

				# --

				self.entity_list.append(s)

				# --

				try:
					self.entity2name[s].add(self.utility.norm_name(self.utility.uri2name(s)))

				except KeyError:
					self.entity2name[s] = set([self.utility.norm_name(self.utility.uri2name(s))])

				# --

				if p == 'http://xmlns.com/foaf/0.1/name':
					'''
					try:
						self.entity2name[s].add(self.utility.norm_name(o))

					except KeyError:
						self.entity2name[s] = set([self.utility.norm_name(o)])
					'''
					pass

				else:
					self.literal_list.append(o)

					# --

					try:
						self.enpair2property[s]

					except KeyError:
						self.enpair2property[s] = {}

					try:
						self.enpair2property[s][o].add(p)

					except KeyError:
						self.enpair2property[s][o] = set([p])

					# --

					try:
						self.p_name2uri[self.utility.uri2name(p)].add(p)

					except KeyError:
						self.p_name2uri[self.utility.uri2name(p)] = set([p])

		# --

		for entity in self.entity_list:
			for name in self.entity2name[entity]:
				try:
					self.name2entity[name].add(entity)

				except KeyError:
					self.name2entity[name] = set([entity])

		# -- 

		self.entity_list = list(set(self.entity_list))
		self.literal_list = list(set(self.literal_list))

	# --

	def complete_type(self):
		for e in self.entity2type.keys():
			for t in set(self.entity2type[e]):
				self.entity2type[e] |= self.get_superclass_set(t)

	def get_superclass_set(self, t):
		superclass_set = set([t])

		curr_t = t

		while True:
			try:
				superclass_set.add(self.subclass2superclass[curr_t])

				curr_t = self.subclass2superclass[curr_t]

			except KeyError:
				break

		return superclass_set

	# --

	def count_property(self):
		for e1 in self.enpair2property.keys():
			for e2 in self.enpair2property[e1].keys():
				for p in self.enpair2property[e1][e2]:
					try:
						self.entity2p_cnt[e1] += 1

					except KeyError:
						self.entity2p_cnt[e1] = 1

					try:
						self.entity2p_cnt[e2] += 1

					except KeyError:
						self.entity2p_cnt[e2] = 1

		# --

		for e in self.entity_list:
			try:
				self.entity2p_cnt[e]

			except KeyError:
				self.entity2p_cnt[e] = 0

	# --

	def get_specific_type(self, entity):
		type_set = set([])

		# --

		if self.utility.is_literal(entity):
			type_set = set([self.utility.is_literal(entity)])

		else:
			try:
				type_set = self.entity2type[entity]

				for t in set(type_set):
					t_superclass_set = self.get_superclass_set(t)

					t_superclass_set.remove(t)

					# --

					type_set = type_set - (t_superclass_set & type_set)

			except KeyError:
				pass

		# --

		return type_set

	# --

	def check_domain_range(self, KB_s, KB_p, KB_o):
		p = self.utility.uri2name(KB_p)

		# --

		try:
			p_domain = self.p_name2domain[p]
		
		except KeyError:
			p_domain = set([])

		try:
			p_range = self.p_name2range[p]

		except KeyError:
			p_range = set([])

		# --

		if self.utility.is_literal(KB_s):
			return False

		else:
			try:
				s_types = self.entity2type[KB_s]

			except KeyError:
				s_types = set([])

		# --

		if self.utility.is_literal(KB_o):
			o_types = set([self.utility.is_literal(KB_o)])

		else:
			try:
				o_types = self.entity2type[KB_o]

			except KeyError:
				o_types = set([])

		# --

		s_valid = False

		if len(p_domain) > 0:
			if len(p_domain & s_types) > 0:
				s_valid = True

			else:
				s_valid = False

		else:
			s_valid = True

		o_valid = False

		if len(p_range) > 0:
			if len(p_range & o_types) > 0:
				o_valid = True

			else:
				o_valid = False

		else:
			o_valid = True

		# --

		if s_valid and o_valid:
			return True

		else:
			return False