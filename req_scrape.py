from bs4 import BeautifulSoup, SoupStrainer
import requests 
import cPickle as pickle
# import the pickling/saving module from main codebase

class Parser(object):
	def __init__(self, url_stem):
		self.url_stem = url_stem

	def setup_soup(self, url_leaf):
		url = self.url_stem + url_leaf
		response = requests.get(url).text
		soup = BeautifulSoup(response, 'lxml', parse_only=SoupStrainer(['tr']))
		return soup

class BreadthParser(Parser):
	def __init__(self):
		self.url_stem = "http://guide.berkeley.edu/undergraduate/colleges-schools/letters-science/breadth-requirement-"
		self.breadths = ["arts-literature", 
					"biological-science", 
					"historical-studies", 
					"international-studies", 
					"philosophy-values", 
					"physical-science", 
					"social-behavioral-sciences"]
		self.abbrevs = {"arts-literature":"al",
					"biological-science":"bs",
					"historical-studies":"hs", 
					"international-studies":"is", 
					"philosophy-values":"pv", 
					"physical-science":"ps", 
					"social-behavioral-sciences":"sbs"}

	def make_req_pickle(self, soup, url_leaf, abbrev):
		# TODO: To convert dept abbrev to full name?
		file_name = abbrev[url_leaf] + ".pickle"
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
		with open(file_name, "wb") as handle:
			pickle.dump(classes, handle)
		return classes

class FLParser(Parser):
	def __init__(self):
		pass

	def make_fl_pickle(self, soup):
		rows = soup.find_all('td')
		fl_classes = {}
		changed_dept = ["SCANDIN", "EAEURST", "SLAVIC", "EAEUR ST"]
		new_dept_abbrev = {"Armenian": "ARMENI",
						   "Bosnian, Croatian, Serbian": "BOSCRSR",
						   "Bulgarian": "BULGARI",
						   "Hungarian","HUNGARI",
						   "Romanian":"ROMANI",
						   "Norwegian":"NORWEGN",
						   }
		for i in range(1, len(rows), 3):
			classes = rows[i].text.split(';')
			classes = ' '.join(classes).split()
			classes = [c.strip(",") for c in classes[1:]]
			dept = classes[0]
			lang = rows[i].previous_sibling.previous.sibling.text
			if dept in changed_dept:
				if lang in new_dept_abbrev:
					dept = new_dept_abbrev[lang]
				else:
					dept = lang.upper()
			fl_classes[dept] = classes[1:]
		with open("fl.pickle", "wb") as handle:
			pickle.dump(fl_classes, handle)
		return fl_classes

def main():	
	p_breadth = Parser("http://guide.berkeley.edu/undergraduate/colleges-schools/letters-science/breadth-requirement-")
	b = BreadthParser()
	url_leafleaf = b.breadths[0] # TODO: will loop later or a better concurrency-related script
	soup = b.setup_soup(url_leaf)
	classes = b.make_req_pickle(soup, url_leaf, b.abbrevs)

	p_lang = Parser("http://engineering.berkeley.edu/student-services/degree-requirements/foreign-language-courses") #UNTESTED


if __name__ == '__main__':
	main()