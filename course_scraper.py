# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re

url = 'http://guide.berkeley.edu/courses/ast'
url_main = 'http://guide.berkeley.edu/courses'
url_stem = 'http://guide.berkeley.edu'
regex = re.compile('/courses/\w+')

setup_response = requests.get(url_main, headers=headers).text
setup = BeautifulSoup(setup_response, 'lxml', parse_only=SoupStrainer('a'))

response = requests.get(url, headers=headers).text
# soup = BeautifulSoup(response, 'lxml', parse_only=SoupStrainer('a'))

soup = BeautifulSoup(response, 'lxml', parse_only=SoupStrainer(['p','div']))

def get_course_links(soup): # links to scrape
	leaves = []
	for link in soup.find_all('a',href=True):
		if re.match(regex, link['href']) is not None:
			leaves.append(link['href'])
	return leaves

def get_course_info(course_info): # TODO, split the class code into dept and course number? more importantly, remove units.
	units_remove = re.compile('Units')
	# for course_info in soup.find_all('p',class_='courseblocktitle'):
	for item in course_info.find_all('span'):
	 	attr = item.attrs['class'][0]
	 	element = item.text
	 	print(attr.title() + ": " + element)

def get_course_desc(course_desc):
	# for course_desc in soup.find_all('p', class_='courseblockdesc'):
	print(course_desc.text)

def get_course_reqs(course_req): # TODO remove unnecessary info
	# for course_req in soup.find_all('div', class_='course-section'):
	course_spacing = " ".join(item.strip() for item in course_req.find_all(text=True))
	repeat_regex_filter = re.compile(course_req.p.text)
	course = re.sub(repeat_regex_filter, '', course_spacing)
	print(course_req.p.text + ": " + course)

def get_all_course(soup):
	for course_info, course_desc, course_req in zip(soup.find_all('p',class_='courseblocktitle'), \
												soup.find_all('p', class_='courseblockdesc'), \
												soup.find_all('div', class_='course-section')):
		get_course_info(course_info)
		get_course_desc(course_desc)
		get_course_reqs(course_req)


if __name__ == '__main__':
	get_all_course(soup)
