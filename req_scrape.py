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
	def __init__(self, b):
		self.url_stem = "http://guide.berkeley.edu/undergraduate/colleges-schools/letters-science/breadth-requirement-"
		self.breadths = {"arts-literature":"al", 
					"biological-science":"bs", 
					"historical-studies":"hs", 
					"international-studies":"is", 
					"philosophy-values":"pv", 
					"physical-science":"ps", 
					"social-behavioral-sciences":"sbs"}
		self.file_name = self.breadths[b]

	def make_req_dict(self, soup, url_leaf, abbrev):
		# TODO: To convert dept abbrev to full name?
		classes = {}
		rows = soup.find_all('tr')
		curr_dept = ""
		for item in rows:
			dept, course_num = item.a['title'].split()
			if dept != curr_dept:
				classes[dept] = [course_num]
				curr_dept = dept
			else:
				classes[dept].append(course_num)
		return classes

class FLParser(Parser):
	def __init__(self):
		self.url_stem = "http://engineering.berkeley.edu/student-services/degree-requirements/foreign-language-courses"

	def make_fl_dict(self, soup):
		rows = soup.find_all('td')
		fl_classes = {}
		changed_dept = ["SCANDIN", "EAEURST", "SLAVIC", "EAEUR ST"]
		new_dept_abbrev = {"Armenian": "ARMENI",
						   "Bosnian, Croatian, Serbian": "BOSCRSR",
						   "Bulgarian": "BULGARI",
						   "Hungarian": "HUNGARI",
						   "Romanian":"ROMANI",
						   "Norwegian":"NORWEGN",
						   }
		for i in range(1, len(rows), 3):
			classes = rows[i].text
			if ';' in classes: 
				semicolon = classes.index(';')
				set1, set2 = classes[:semicolon], classes[semicolon+1:]
				set1 = ''.join(set1.strip(',')).strip().split()
				set2 = ''.join(set2.strip(',')).strip().split() #move to some kind of tools file
				dept1, dept2 = set1[0], set2[0]
				fl_classes[dept1] = set1[1:]
				fl_classes[dept2] = set2[1:]
			lang = rows[i].previous_sibling.previous.sibling.text
			if dept in changed_dept:
				if lang in new_dept_abbrev:
					dept = new_dept_abbrev[lang]
				else:
					dept = lang.upper()
			fl_classes[dept] = classes[1:]
		return fl_classes	

def main():	
	pass
	# TODO: unit tests


if __name__ == '__main__':
	main()