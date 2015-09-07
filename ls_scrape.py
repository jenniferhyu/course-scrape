from bs4 import BeautifulSoup, SoupStrainer
import requests 
import cPickle as pickle

class Parser(object):
	def __init__(self, url_stem="http://guide.berkeley.edu/undergraduate/colleges-schools/letters-science/breadth-requirement-"):
		self.url_stem = url_stem

	def setup_soup(self, url_leaf):
		url = self.url_stem + url_leaf
		response = requests.get(url).text
		soup = BeautifulSoup(response, 'lxml', parse_only=SoupStrainer(['tr']))
		return soup

class BreadthParser(Parser): # maybe use Parser
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
		stop_counter = 0
		for item in rows:
			stop_counter += 1
			dept, course_num = item.a['title'].split()
			if dept != curr_dept:
				classes[dept] = [course_num]
				curr_dept = dept
			else:
				classes[dept].append(course_num)
		with open(file_name, "wb") as handle:
			pickle.dump(classes, handle)
		return classes

def main():	
	p = Parser()
	b = BreadthParser()
	url_leafleaf = b.breadths[0] # will loop later or a better concurrency-related script
	soup = b.setup_soup(url_leaf)
	classes = b.make_req_pickle(soup, url_leaf, b.abbrevs)

if __name__ == '__main__':
	main()