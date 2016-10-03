#!/usr/bin/python3


def load_fields(file_name):

	fil = open(file_name,'r')
	data = fil.read().replace('\n','')
	fil.close()
	d = [elm.lstrip('[') for elm in data.split(']') if elm!='']
	out = {}
	for entry in d:
		e = [[t.strip().lower() for t in elm.split("=")] for elm in entry.split(";") if elm != '']
		tmp_dict = {}
		for key,value in e:
			if key == "keyword":
				if value in out:
					raise ValueError
				keyword = value
			else:
				tmp_dict[key] = value
		out[keyword] = tmp_dict
	for key in out:
		out[key]['required'] = [elm for elm in out[key]['required'].split(',') if elm != '']
		try:
			out[key]['optional'] = [elm for elm in out[key]['optional'].split(',') if elm != '']
		except KeyError:
			pass
	return out


def create_entry(fields,keyword,data):
	omit = []
	for key in fields[keyword]['optional']:
		if key not in data:
			omit.append(key)
	field_data = fields[keyword]['format'].split("'")

	optional_locations = []

	for elm in [[t.strip("}") for t in elm.split("{")] for elm in field_data[1::2]]:
		for t in elm:
			if t in fields[keyword]['optional']:
				optional_locations.append(t)
				continue

	omit_indices = [2*optional_locations.index(elm)+1 for elm in omit]
	
	print("".join([elm for elm in field_data if field_data.index(elm) not in omit_indices]).format(**data))
	



if __name__ == "__main__":

	file_name = "cv_formatting.txt"
	fields = load_fields(file_name)

	test_data = {'university':'Texas A\&M University','degree':'Ph.D','state':'TX','city':'College Station',
'begin':'September 2009','end':'May 2015'}



	create_entry(fields,'education',test_data)

	"""
	omit = []
	for key in fields['education']['optional']:
		if key not in test_data:
			omit.append(key)


	field_data = fields['education']['format'].split("'")

	optional_locations = []

	for elm in [[t.strip("}") for t in elm.split("{")] for elm in field_data[1::2]]:
		for t in elm:
			if t in fields['education']['optional']:
				optional_locations.append(t)
				continue

	omit_indices = [2*optional_locations.index(elm)+1 for elm in omit]
	
	print("".join([elm for elm in field_data if field_data.index(elm) not in omit_indices]).format(**test_data))
	"""



















