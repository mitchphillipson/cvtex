from base_create import *

class MiniCV(CV):
    """Only create the CV using entries that have "small=True" """

	def to_appear(self,data):	
		return data.small



if __name__=='__main__':
	

	formatting_file= "cv_formatting.txt"

	data_file = "cv_data.txt"

	test = MiniCV(data_file,formatting_file)
	
	test.create_cv('output/mini_cv.tex')
