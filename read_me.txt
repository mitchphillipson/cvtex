This is a Python3 package used to create a CV much in the style of BibTex. This was created because
the author was sick of maintaining three separate CV files (Long form, short form and HTML). 

Files:

base_create.py ->   Contains the base classes used for constructing the CV. It currently defaults to 
                    creating the CV in LaTeX, it will need to be updated to be more dynamic (including
                    HTML).

                    Additionally, the sections and order are currently hard coded. It won't include
                    any fields that aren't present in "self.sections". However, it shouldn't break
                    if they aren't present in the fields document (but it might). Eventually, this
                    can be made more dynamic by taking fields and order from "cv_formatting.txt". 

                    It's safe to run this file, it will return a long form CV with all fields that
                    do not have the flag "show=False".


cv_formatting.py -> This should be relatively set and shouldn't need improvement. It contains methods
                    to load the fields and formatting data.

field.py ->         The container class for a field. The DataEntry is the base class that is generic,
                    most fields belong in this class. There are a couple of specialized classes that
                    may no longer be necessary. This class also contains order information.

cv_formatting.txt-> This contains the individual fields that make up how the CV looks. The format 
                    string "{  }" denotes keywords and '  ' denotes optional entries. 

header.txt,footer.txt -> The header and footer of the CV tex file. Change to modify appearance of your
                         CV.

cv_data.txt ->      All the data of your CV. Each entry should be in {} with semicolons at the end of  
                    lines.
