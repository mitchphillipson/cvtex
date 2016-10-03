#!/usr/bin/python3


from field import *



BASELINESKIP = .5

latex_replacements = {"~":"$\sim$","&":"\\&"}


def load_fields(file_name,replacement_dict={}):
	"""
	Input: file_name -> string: location of data file.
	
	Output: dicitonary -> key: keyword given in file (lower case) 
						  value: Instance of Field class
	"""
	fil = open(file_name,'r')
	data = fil.read().replace('\n','')
	fil.close()
	d = [elm.lstrip('[') for elm in data.split(']') if elm!='']
	field_list = []
	for entry in d:
		e = [[t.strip().lower() for t in elm.split("=")] for elm in entry.split(";") if elm != '']
		tmp_dict = {}
		for key,value in e:
			tmp_dict[key] = value
		field_list.append(tmp_dict)
	for field in field_list:
		field['required'] = [elm for elm in field['required'].split(',') if elm != '']
		try:
			field['optional'] = [elm for elm in field['optional'].split(',') if elm != '']
		except KeyError:
			pass
	out = {}
	for field in field_list:
		keyword = field['keyword']
		if keyword in out:
			raise KeyError("'{0}' already exists as a keyword".format(keyword))
		out[keyword] = Field(field,replacement_dict)
	return out
	

def load_data(file_name,fields):
	"""
	Input: file_name -> string: location of data file.
	
	Output: dicitonary -> key: keyword given in file (lower case) 
						  value: list of dicionaries of data
	"""
	fil = open(file_name,'r')
	data = fil.read().replace('\n','')
	fil.close()
	d = [elm.lstrip('{') for elm in data.split('}') if elm!='']
	out = {}
	for key in fields:
		out[key] = []
	for entry in d:
		e = [[t.strip() for t in elm.split("=")] for elm in entry.split(";") if elm != '']
		tmp_dict = {}
		for key,value in e:
			tmp_dict[key.lower()] = value
		keyword = tmp_dict['keyword']
		field = fields[keyword]
		out[keyword].append(field(tmp_dict))
	return out




class CV(object):
	
	def __init__(self,data_file,formatting_file,HTML = False):

		self.fields = load_fields(formatting_file,latex_replacements)
		self.data = load_data(data_file,self.fields)
		#for key in self.data:
		#	self.data[key].sort(key=entry_order)

		#Add keyword:Section names here. Order is unimportant.
		self.sections = {	'education':"Education",
							'address':"Address",
							'publication':"Publications",
							'work experience':"Work Experience",
							'award':"Awards and Honors",
							'grant':"Grants",
							'talk conference':"Presentations",
							'conference':"Workshops and Conferences",
							'organization':"Organizations",
							'undergraduate research':"Undergraduate Research",
							'poster':"Selected Posters",
							'undergraduate presentation':"Selected Undergraduate Presentations",
							'outreach':"Outreach",
							'mentoring':"Mentoring",
						}
		

		#Move stuff around here to change order, or comment out to remove.
		self.cv_order = [	'address',
							'education',
							'work experience',
							'mentoring',
							'outreach',
							'award',
							'grant',
							'publication',
							'talk conference',
							'conference',
							'organization',
							'undergraduate research',
							'poster',
							'undergraduate presentation'
						]

	def create_cv(self,output_file):
		head = open("header.tex",'r')
		cv = head.read()
		head.close()

		for key in self.cv_order:
			self.data[key].sort(reverse = True)
			if all([not self.to_appear(elm) for elm in self.data[key]]):
				continue

			#Change this line to change section styles.
			cv += "\\section{{\\textbf{{\\large {0}}}}}".format(self.sections[key]) 

			if key not in self.data:
				continue
			for d in self.data[key]:
				if self.to_appear(d):
					cv += str(d)
					cv += "\\vspace{{{0}\\baselineskip}}\n\n\n".format(BASELINESKIP)
			cv += "\n\n\n"	

		foot = open('footer.tex','r')
		cv += foot.read()
		foot.close()

		out = open(output_file,'w')
		out.write(cv)
		out.close()


	def to_appear(self,data):
		return data.show







if __name__=='__main__':
	

	formatting_file= "cv_formatting.txt"

	data_file = "cv_data.txt"

	test = CV(data_file,formatting_file)
	
	test.create_cv('output/cv.tex')
	











































