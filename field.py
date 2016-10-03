#!/usr/bin/python3


time_list = [	'Winter','January','February','Spring','March','April','May','Summer','June'
		,'July','August','Fall','September','October','November','December','Current'
		,'Present']

special_fields = {} #Whenever a new DataEntry is created, add keyword:class to this


class DataEntry(object):

	def __init__(self,field,data):
		self.field = field
		self.data = data
		try:
			html = data['html']
			if html.lower() == 'true':
				self.html = True
			else:
				self.html = False
		except KeyError:
			self.html = False
		try:
			small = data['small']
			if small.lower() == 'true':
				self.small = True
			else:
				self.small = False
		except KeyError:
			self.small = False
		try:
			show = data['show']
			if show.lower() == 'true':
				self.show = True
			else:
				self.show = False
		except KeyError:
			self.show = True

	def __str__(self):
		return self.field.data_format(self.data)

	def __lt__(self,f):
		try:
			test1 = self.data['end']
		except KeyError:
			test1 = self.data['begin']
		try:
			test2 = f.data['end']
		except KeyError:
			test2 = f.data['begin']
		try:
			st1,year1 = test1.split(' ')
		except ValueError:
			st1 = test1
			year1 = 5000 #Put this first
		try:
			st2,year2 = test2.split(' ')
		except ValueError:
			st2 = test2
			year2 = 5000 #Put this first
	
		year1 = int(year1)
		year2 = int(year2)
		ind1 = time_list.index(st1)
		ind2 = time_list.index(st2)

		return (year1,ind1)<(year2,ind2)


class PublicationEntry(DataEntry):
	
	def __lt__(self,f):
		y1 = int(self.data['year'])
		y2 = int(f.data['year'])
		return y1<y2

special_fields['publication'] = PublicationEntry

class EducationEntry(DataEntry):

	def __lt__(self,field):
		return self.data['degree']<field.data['degree']

special_fields['education'] = EducationEntry




class Field(object):

	def __init__(self,format_dict,replacement_dict = {}):
		self.keyword = format_dict['keyword']
		self.required = format_dict['required']
		self.optional = format_dict['optional']
		self.format = format_dict['format']

		self.replacement_dict = replacement_dict

		self.data_type = DataEntry if self.keyword not in special_fields else special_fields[self.keyword]

			
		

	def __call__(self,data_dict):
		for key in self.required:
			if key not in data_dict:
				error_string = "'{0}' is a required value for keyword '{1}'. Data dump: {2}".format(key,self.keyword,data_dict)
				raise KeyError(error_string)
		return self.data_type(self,data_dict)

	def data_format(self,data_dict):
		omit = []
		for key in self.optional:
			if key not in data_dict:
				omit.append(key)
		field_data = self.format.split("'")

		optional_locations = []

		for elm in [[t.split("}")[0] for t in elm.split("{")] for elm in field_data[1::2]]:
			for t in elm:
				if t in self.optional:
					optional_locations.append(t)
					continue

		omit_indices = [2*optional_locations.index(elm)+1 for elm in omit]
		tmp = "".join([elm for elm in field_data if field_data.index(elm) not in omit_indices])
		tmp = tmp.format(**data_dict)
		for key in self.replacement_dict:
			tmp = tmp.replace(key,self.replacement_dict[key])
		return tmp

		







if __name__=='__main__':
	
	test_format = {'keyword':'education','required':['title','begin'],
				   'optional':['end'],'format':"{title}, {begin}'--{end}'"}

	test_data = {'keyword':'education','title':'Ph.d','begin':'September 2011','end':'May 2015'}

	t = Field(test_format)

	print(t(test_data))








