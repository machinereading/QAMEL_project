class utility:
	def uri2name(self, uri):
		if self.is_literal(uri):
			return uri

		# --
		
		import re

		name = re.split(r'[/#:]', uri)[-1]

		# --

		if name == 'class':
			name = 'class_'

		# --
		
		return name

	def name2uri(self, name, uri_set):
		for uri in uri_set:
			if name == self.uri2name(uri):
				return uri

		return name

	def norm_name(self, name):
		import re

		# 공백 제거
		norm = re.sub(r'[_\s]', '', name)

		# 소문자화
		norm = norm.lower()

		return norm

	def is_literal(self, text):
		text = text.strip()

		# == KB 형태 리터럴인지 검사

		# -- date

		import re

		match = re.findall(r'^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}$', text)

		if len(match) > 0:
			return 'date'

		# -- time

		match = re.findall(r'^(?:[0-9]{1,2}:)?(?:[0-9]{1,2}:)?[0-9]{1,2}(?:\.[0-9]+)?$', text)

		if len(match) > 0:
			return 'time'

		# -- float

		import re

		match = re.findall(r'^[0-9]+\.[0-9]+$', text)

		if len(match) > 0:
			return 'float'

		# -- integer

		match = re.findall(r'^[0-9]+$', text)

		if len(match) > 0:
			return 'integer'

		# == 표면형 형태 리터럴인지 검사

		# -- 날짜

		match = re.findall(r'^([0-9]{4})\s*년\s*([0-9]{1,2})\s*월\s*([0-9]{1,2})\s*일$', text)

		if len(match) > 0:
			return 'surface-date'

		# --

		match = re.findall(r'^그저께$', text)

		if len(match) > 0:
			return 'surface-date'

		# --

		match = re.findall(r'^어제$', text)

		if len(match) > 0:
			return 'surface-date'

		# --

		match = re.findall(r'^오늘$', text)

		if len(match) > 0:
			return 'surface-date'

		# --

		match = re.findall(r'^내일$', text)

		if len(match) > 0:
			return 'surface-date'

		# --

		match = re.findall(r'^모레$', text)

		if len(match) > 0:
			return 'surface-date'

		# --

		match = re.findall(r'^([0-9]{1,2})\s*일$', text)

		if len(match) > 0:
			return 'surface-date'

		# --

		match = re.findall(r'^지난\s*([0-9]{1,2})\s*일$', text)

		if len(match) > 0:
			return 'surface-date'

		# --

		match = re.findall(r'^(?:다음|오는)\s*?([0-9]{1,2})\s*일$', text)

		if len(match) > 0:
			return 'surface-date'

		# --

		match = re.findall(r'^지난달\s*([0-9]{1,2})\s*일$', text)

		if len(match) > 0:
			return 'surface-date'

		# --

		match = re.findall(r'^다음달\s*([0-9]{1,2})\s*일$', text)

		if len(match) > 0:
			return 'surface-date'

		# -- 시간

		match = re.findall(r'^([0-9]{1,2})\s*시\s*([0-9]{1,2})\s*분$', text)

		if len(match) > 0:
			return 'surface-time'

		# --

		match = re.findall(r'^오전\s*([0-9]{1,2})\s*시\s*(?:([0-9]{1,2})\s*분)?$', text)

		if len(match) > 0:
			return 'surface-time'

		# --

		match = re.findall(r'^(?:오후|낮|밤)\s*([0-9]{1,2})\s*시\s*(?:([0-9]{1,2})\s*분)?$', text)

		if len(match) > 0:
			return 'surface-time'

		# -- 기록 - 시간

		match = re.findall(r'^(?:([0-9]{1,2})\s*시간)?\s*(?:([0-9]{1,2})\s*분)?\s*([0-9]{1,2})\s*초(?:\s*([0-9]+))?$', text)

		if len(match) > 0:
			return 'surface-time-record'

		# --

		match = re.findall(r'^(?:(?:([0-9]{1,2})\s*:)?\s*(?:([0-9]{1,2})\s*:))?\s*([0-9]{1,2})\s*(?:\s*\.([0-9]+))?$', text)

		if len(match) > 0:
			return 'surface-time-record'

		# -- 기록 - 점수

		match = re.findall(r'^([0-9]+)(?:\.([0-9]+))?\s*점$', text)

		if len(match) > 0:
			return 'surface-score-record'

		# -- 기록 - 순위

		match = re.findall(r'^([0-9]+)\s*위$', text)

		if len(match) > 0:
			return 'surface-rank'

		# --

		return False

	def norm_literal(self, surface_literal, article_info):
		surface_literal = surface_literal.strip()

		norm = surface_literal

		# == 리터럴 표면형 정규화

		# -- 날짜

		import re

		match = re.findall(r'^([0-9]{4})\s*년\s*([0-9]{1,2})\s*월\s*([0-9]{1,2})\s*일$', surface_literal)

		if len(match) > 0:
			year = int(match[0][0].strip())
			month = int(match[0][1].strip())
			day = int(match[0][2].strip())

			norm = '{0:04d}-{1:02d}-{2:02d}'.format(year, month, day)

			return norm

		# --

		match = re.findall(r'^그저께$', surface_literal)

		if len(match) > 0:
			article_match = re.findall(r'^([0-9]{4})-([0-9]{2})-([0-9]{2})$', article_info['date'])

			if len(article_match) > 0:
				a_year = int(article_match[0][0])
				a_month = int(article_match[0][1])
				a_day = int(article_match[0][2])

				if a_month in [1]:
					if a_day == 2:
						a_year -= 1
						a_month = 12
						a_day = 31

					elif a_day == 1:
						a_year -=1
						a_month = 12
						a_day = 30

					else:
						a_day -= 2

				elif a_month in [3]:
					if a_day in [1, 2]:
						return norm

					else:
						a_day -= 2

				elif a_month in [2, 4, 6, 8, 9, 11]:
					if a_day == 2:
						a_month -= 1
						a_day = 31

					elif a_day == 1:
						a_month -= 1
						a_day = 30

					else:
						a_day -= 2

				elif a_month in [5, 7, 10, 12]:
					if a_day == 2:
						a_month -= 1
						a_day = 30

					elif a_day == 1:
						a_month -= 1
						a_day = 29

					else:
						a_day -= 2

				norm = '{0:04d}-{1:02d}-{2:02d}'.format(a_year, a_month, a_day)

				return norm

		match = re.findall(r'^어제$', surface_literal)

		if len(match) > 0:
			article_match = re.findall(r'^([0-9]{4})-([0-9]{2})-([0-9]{2})$', article_info['date'])

			if len(article_match) > 0:
				a_year = int(article_match[0][0])
				a_month = int(article_match[0][1])
				a_day = int(article_match[0][2])

				if a_month in [1]:
					if a_day == 1:
						a_year -= 1
						a_month = 12
						a_day = 31

					else:
						a_day -= 1

				elif a_month in [3]:
					if a_day == 1:
						return norm

					else:
						a_day -= 1

				elif a_month in [2, 4, 6, 8, 9, 11]:
					if a_day == 1:
						a_month -= 1
						a_day = 31

					else:
						a_day -= 1

				elif a_month in [5, 7, 10, 12]:
					if a_day == 1:
						a_month -= 1
						a_day = 30

					else:
						a_day -= 1

				norm = '{0:04d}-{1:02d}-{2:02d}'.format(a_year, a_month, a_day)

				return norm

		match = re.findall(r'^오늘$', surface_literal)

		if len(match) > 0:
			article_match = re.findall(r'^([0-9]{4})-([0-9]{2})-([0-9]{2})$', article_info['date'])

			if len(article_match) > 0:
				a_year = int(article_match[0][0])
				a_month = int(article_match[0][1])
				a_day = int(article_match[0][2])

				norm = '{0:04d}-{1:02d}-{2:02d}'.format(a_year, a_month, a_day)

				return norm

		match = re.findall(r'^내일$', surface_literal)

		if len(match) > 0:
			article_match = re.findall(r'^([0-9]{4})-([0-9]{2})-([0-9]{2})$', article_info['date'])

			if len(article_match) > 0:
				a_year = int(article_match[0][0])
				a_month = int(article_match[0][1])
				a_day = int(article_match[0][2])

				if a_month in [12]:
					if a_day == 31:
						a_year += 1
						a_month = 1
						a_day = 1

					else:
						a_day += 1

				elif a_month in [2]:
					if a_day in [28, 29]:
						return norm

					else:
						a_day += 1

				elif a_month in [3, 5, 7, 8, 10]:
					if a_day == 31:
						a_month += 1
						a_day = 1

					else:
						a_day += 1

				elif a_month in [4, 6, 9, 11]:
					if a_day == 30:
						a_month += 1
						a_day = 1

					else:
						a_day += 1

				norm = '{0:04d}-{1:02d}-{2:02d}'.format(a_year, a_month, a_day)

				return norm

		match = re.findall(r'^모레$', surface_literal)

		if len(match) > 0:
			article_match = re.findall(r'^([0-9]{4})-([0-9]{2})-([0-9]{2})$', article_info['date'])

			if len(article_match) > 0:
				a_year = int(article_match[0][0])
				a_month = int(article_match[0][1])
				a_day = int(article_match[0][2])

				if a_month in [12]:
					if a_day == 31:
						a_year += 1
						a_month = 1
						a_day = 2

					if a_day == 30:
						a_year += 1
						a_month = 1
						a_day = 1

					else:
						a_day += 2

				elif a_month in [2]:
					if a_day in [27, 28, 29]:
						return norm

					else:
						a_day += 2

				elif a_month in [3, 5, 7, 8, 10]:
					if a_day == 31:
						a_month += 1
						a_day = 2

					if a_day == 30:
						a_month += 1
						a_day = 1

					else:
						a_day += 2

				elif a_month in [4, 6, 9, 11]:
					if a_day == 30:
						a_month += 1
						a_day = 2

					if a_day == 30:
						a_month += 1
						a_day = 1

					else:
						a_day += 2

				norm = '{0:04d}-{1:02d}-{2:02d}'.format(a_year, a_month, a_day)

				return norm

		# --

		match = re.findall(r'^([0-9]{1,2})\s*일$', surface_literal)

		if len(match) > 0:
			article_match = re.findall(r'^([0-9]{4})-([0-9]{2})-([0-9]{2})$', article_info['date'])

			if len(article_match) > 0:
				a_year = int(article_match[0][0])
				a_month = int(article_match[0][1])

				day = int(match[0])

				norm = '{0:04d}-{1:02d}-{2:02d}'.format(a_year, a_month, day)

				return norm

		match = re.findall(r'^지난\s*([0-9]{1,2})\s*일$', surface_literal)

		if len(match) > 0:
			article_match = re.findall(r'^([0-9]{4})-([0-9]{2})-([0-9]{2})$', article_info['date'])

			if len(article_match) > 0:
				a_year = int(article_match[0][0])
				a_month = int(article_match[0][1])
				a_day = int(article_match[0][2])

				day = int(match[0])

				if a_day < day:
					if a_month == 1:
						a_year -= 1
						a_month = 12

					else:
						a_month -= 1

				norm = '{0:04d}-{1:02d}-{2:02d}'.format(a_year, a_month, day)

				return norm

		match = re.findall(r'^(?:다음|오는)\s*?([0-9]{1,2})\s*일$', surface_literal)

		if len(match) > 0:
			article_match = re.findall(r'^([0-9]{4})-([0-9]{2})-([0-9]{2})$', article_info['date'])

			if len(article_match) > 0:
				a_year = int(article_match[0][0])
				a_month = int(article_match[0][1])
				a_day = int(article_match[0][2])

				day = int(match[0])

				if day < a_day:
					if a_month == 12:
						a_year += 1
						a_month = 1

					else:
						a_month += 1

				norm = '{0:04d}-{1:02d}-{2:02d}'.format(a_year, a_month, day)

				return norm

		# --

		match = re.findall(r'^지난달\s*([0-9]{1,2})\s*일$', surface_literal)

		if len(match) > 0:
			article_match = re.findall(r'^([0-9]{4})-([0-9]{2})-([0-9]{2})$', article_info['date'])

			if len(article_match) > 0:
				a_year = int(article_match[0][0])
				a_month = int(article_match[0][1])

				if a_month == 1:
					a_year -= 1
					a_month = 12

				else:
					a_month -= 1

				day = int(match[0])

				norm = '{0:04d}-{1:02d}-{2:02d}'.format(a_year, a_month, day)

				return norm

		# --

		match = re.findall(r'^다음달\s*([0-9]{1,2})\s*일$', surface_literal)

		if len(match) > 0:
			article_match = re.findall(r'^([0-9]{4})-([0-9]{2})-([0-9]{2})$', article_info['date'])

			if len(article_match) > 0:
				a_year = int(article_match[0][0])
				a_month = int(article_match[0][1])

				if a_month == 12:
					a_year += 1
					a_month = 1

				else:
					a_month += 1

				day = int(match[0])

				norm = '{0:04d}-{1:02d}-{2:02d}'.format(a_year, a_month, day)

				return norm

		# -- 시간

		match = re.findall(r'^([0-9]{1,2})\s*시\s*([0-9]{1,2})\s*분$', surface_literal)

		if len(match) > 0:
			hour = int(match[0][0].strip())
			minute = int(match[0][1].strip())

			norm = '{0:02d}:{1:02d}'.format(hour, minute)

			return norm

		match = re.findall(r'^오전\s*([0-9]{1,2})\s*시\s*(?:([0-9]{1,2})\s*분)?$', surface_literal)

		if len(match) > 0:
			hour = int(match[0][0].strip())

			if hour == 12:
				hour = 0

			try:
				minute = int(match[0][1].strip())

			except:
				minute = 0

			norm = '{0:02d}:{1:02d}'.format(hour, minute)

			return norm

		match = re.findall(r'^(?:오후|낮|밤)\s*([0-9]{1,2})\s*시\s*(?:([0-9]{1,2})\s*분)?$', surface_literal)

		if len(match) > 0:
			hour = int(match[0][0].strip())

			if hour != 12:
				hour += 12

			try:
				minute = int(match[0][1].strip())

			except:
				minute = 0

			norm = '{0:02d}:{1:02d}'.format(hour, minute)

			return norm

		# -- 기록 - 시간

		match = re.findall(r'^(?:([0-9]{1,2})\s*시간)?\s*(?:([0-9]{1,2})\s*분)?\s*([0-9]{1,2})\s*초(?:\s*([0-9]+))?$', surface_literal)

		if len(match) > 0:
			try:
				hour = int(match[0][0].strip())

			except:
				hour = 0.0

			try:
				minute = int(match[0][1].strip())

			except:
				minute = 0.0

			second = int(match[0][2].strip())

			try:
				milisecond = float('0.' + match[0][3].strip())

			except:
				milisecond = 0.0

			second += milisecond

			norm = str(round(hour * 3600.0 + minute * 60.0 + second, 3))

			return norm

		# --
		
		match = re.findall(r'^(?:(?:([0-9]{1,2})\s*:)?\s*(?:([0-9]{1,2})\s*:))?\s*([0-9]{1,2})\s*(?:\s*\.([0-9]+))?$', surface_literal)

		if len(match) > 0:
			try:
				hour = int(match[0][0].strip())

			except:
				hour = 0.0

			try:
				minute = int(match[0][1].strip())

			except:
				minute = 0.0

			second = int(match[0][2].strip())

			try:
				milisecond = float('0.' + match[0][3].strip())

			except:
				milisecond = 0.0

			second += milisecond

			norm = str(round(hour * 3600.0 + minute * 60.0 + second, 3))

			return norm

		# -- 기록 - 점수

		match = re.findall(r'^([0-9]+)(?:\.([0-9]+))?\s*점$', surface_literal)

		if len(match) > 0:
			if len(match[0][1]) > 0:
				score_1 = float(match[0][0])
				score_2 = float('0.' + match[0][1])

			else:
				score_1 = int(match[0][0])
				score_2 = 0

			norm = str(score_1 + score_2)

			return norm

		# -- 기록 - 순위

		match = re.findall(r'^([0-9]+)\s*위$', surface_literal)

		if len(match) > 0:
			rank = match[0]
			
			norm = rank

			return norm

		# --

		return norm

	def norm_article_date(self, date):
		# 네이버 스포츠: 2014.02.18 오후 09:02
		# 네이버 연예: 2014.02.16 오후 4:00
		# 네이버 뉴스: 2014-02-17 17:43

		date = date.strip()

		# --

		norm = date

		# --

		import re

		match = re.findall(r'^([0-9]{4})[.-]([0-9]{1,2})[.-]([0-9]{1,2})\s+.+$', date)

		if len(match) > 0:
			year = match[0][0]
			month = match[0][1]
			day = match[0][2]

			# --

			norm = '-'.join([year, month, day])

		# --

		return norm