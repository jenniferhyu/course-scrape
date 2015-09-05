from scrapy.spiders import Spider, CrawlSpider, Rule
from catalog.items import CatalogItem
from scrapy.linkextractors import LinkExtractor
import re
from bs4 import BeautifulSoup

class CoursesSpider(CrawlSpider):
	name = 'courses'
	allowed_domains = ['guide.berkeley.edu']
	start_urls = ['http://guide.berkeley.edu/courses/']
	rules = [Rule(LinkExtractor(allow=(r'/courses/ast\b')), callback='parse_item', follow=True)] # restricted to test site on AST
	# TODO: regex need to include commas

	def parse_item(self, response):
		courses = response.xpath('//*[@id="courseinventorycontainer"]/div/div')
		for c in courses:
			soup = BeautifulSoup(c.extract(), 'lxml')
			item = CatalogItem()
			item['dept'], item['class_num'] = c.xpath('./p/a/span[1]/text()').extract()[0].split()
			item['full_dept'], item['course_level'] = self.get_subject_course(c, soup) 
			item['title'] = c.xpath('./p/a/span[2]/text()').extract()[0]
			item['units'] = self.parse_units(c)
			item['description'] = self.get_description(c)[1]
			item['fall'], item['spring'] = self.find_terms_offered(self.get_description(c))
			item['prereqs'] = self.get_prereqs(c, soup)
			item['cross_list'] = self.get_cross_list(c, soup)
			item['grading'], item['final_exam'] = self.get_grading_option(c, soup)
			item['format'] = self.get_class_format(c, soup)
			item['previously'] = self.get_previously(c, soup)
			yield item

	def parse_units(self, course):
		units_regex = ur'\d+\s(-\s\d+)?' # regex for cases when `1 - 12 units` or `3 units`
		units_temp = course.xpath('./p/a/span[3]/text()').extract()[0]
		num_units = re.match(units_regex, units_temp).group(0).strip()
		return num_units

	def get_description(self, course):
		return ''.join(course.xpath('./div/p//text()').extract()).strip().split('\n')

	def find_terms_offered(self, description): # make default description 
		terms = description[0]
		terms = re.sub(ur'Terms offered: ', '', terms).split()
		fall_spring = [False, False]
		for t in terms:
			if not t.isdigit():
				if t == 'Fall':
					fall_spring[0] = True
				elif t == 'Spring':
					fall_spring[1] = True
				else:
					continue # we're not counting summer for now
		return fall_spring

	def get_prereqs(self, course, soup):
		prereqs_body = soup.body.find(text='Prerequisites:')
		if prereqs_body:
			return prereqs_body.next_element.strip()

	def get_subject_course(self, course, soup):
		course_body = soup.body.find(text='Subject/Course Level:')
		if course_body:
			return course_body.next_element.strip().split('/')

	def get_cross_list(self, course, soup):
		cross_list_body = soup.body.find(text='Also listed as:')
		if cross_list_body:
			return cross_list_body.next_element.strip()

	def get_grading_option(self, course, soup):
		grading_option = soup.body.find(text=re.compile(ur'Grading.*'))
		if grading_option:
			split_arr = grading_option.next_element.strip().split('.')
			return split_arr

	def get_class_format(self, course, soup):
		class_format_body = soup.body.find(text='Hours & Format')
		if class_format_body: # sanity check
			return class_format_body.next_element.text

	def get_previously(self, course, soup):
		previously_body = soup.body.find(text='Formerly known as:')
		if previously_body:
			return previously_body.next_element.strip()

	#TODO: get credit_options