from bs4 import BeautifulSoup, SoupStrainer
import requests 
import cPickle as pickle

def setup_soup():
	url_stem = 'http://guide.berkeley.edu/undergraduate/colleges-schools/letters-science/breadth-requirement-'
	breadths = ["arts-literature", 
				"biological-science", 
				"historical-studies", 
				"international-studies", 
				"philosophy-values", 
				"physical-science", 
				"social-behavioral-sciences"]
	url = url_stem + breadths[0]
	response = requests.get(url).text
	soup = BeautifulSoup(response, 'lxml', parse_only=SoupStrainer(['tr']))
	return soup

def get_course_code(soup):
	class_codes = [] #massive array!
	rows = soup.find_all('tr')
	for item in rows:
		class_codes.append(item.td.text)