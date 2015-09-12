from bs4 import BeautifulSoup, SoupStrainer
import requests 
import cPickle as pickle
# import the pickling/saving module from main codebase

class Parser(object):
	def __init__(self):
		pass

	def setup_soup(self, url_leaf):
		url = self.url_stem + url_leaf
		response = requests.get(url).text
		soup = BeautifulSoup(response, 'lxml', parse_only=SoupStrainer(['tr']))
		return soup

	def pickler(self, dict_dump, file_name):
		with open(file_name+".pickle", "wb") as handle:
			pickle.dump(dict_dump, handle)

class BreadthParser(Parser):
	def __init__(self, index):
		self.url_stem = "http://guide.berkeley.edu/undergraduate/colleges-schools/letters-science/breadth-requirement-"
		self.breadths = {"arts-literature":"al", 
					"biological-science":"bs", 
					"historical-studies":"hs", 
					"international-studies":"is", 
					"philosophy-values":"pv", 
					"physical-science":"ps", 
					"social-behavioral-sciences":"sbs"}
		self.url_leaf = self.breadths.keys()[index]
		self.file_name = self.breadths[self.url_leaf]
		self.reqs = {}

	def make_req_dict(self, soup, abbrev):
		# TODO: To convert dept abbrev to full name?
		rows = soup.find_all('tr')
		curr_dept = ""
		for item in rows:
			dept, course_num = item.a['title'].split()
			if dept != curr_dept:
				self.reqs[dept] = [course_num]
				curr_dept = dept
			else:
				self.reqs[dept].append(course_num)
		return self.reqs

class FLParser(Parser):
	def __init__(self):
		self.url_stem = "http://engineering.berkeley.edu/student-services/degree-requirements/foreign-language-courses"
		self.file_name = "fl"
		self.changed_dept = ["SCANDIN", "EAEURST", "SLAVIC", "EAEUR ST"]
		self.new_dept_abbrev = {"Armenian": "ARMENI",
						   "Bosnian, Croatian, Serbian": "BOSCRSR",
						   "Bulgarian": "BULGARI",
						   "Hungarian": "HUNGARI",
						   "Romanian":"ROMANI",
						   "Norwegian":"NORWEGN",
						   }
		self.fl_classes = {}

	def make_fl_dict(self, soup):
		rows = soup.find_all('td')
		for i in range(1, len(rows), 3):
			classes = rows[i].text			
			if ';' in classes: 
				"""Parses the IRANIAN 110A; PERSIAN 1A, 1B, 11A, 11B, 100A, 100B type cases"""
				semicolon = classes.index(';')
				set1, set2 = classes[:semicolon], classes[semicolon+1:]
				set1 = ''.join(set1.strip(',')).strip().split()
				set2 = ''.join(set2.strip(',')).strip().split() #move to some kind of tools file
				dept1, dept2 = set1[0], set2[0]
				self.fl_classes[dept1] = set1[1:]
				self.fl_classes[dept2] = set2[1:]
			else:
				classes = classes.split()
				dept_key = classes[0]
				codes = ''.join(classes[1:]).split(',')
				lang = rows[i].previous_sibling.previous.sibling.text
				if dept_key in self.changed_dept:
					dept_key = dept_change(dept_key, lang)
				self.fl_classes[dept_key] = codes
		return fl_classes	

	def dept_change(self, dept, lang):
		if lang in self.new_dept_abbrev:
			dept = self.new_dept_abbrev[lang]
		else:
			dept = lang.upper()
		return dept

def main():	
	pass
	# TODO: unit tests

if __name__ == '__main__':
	main()