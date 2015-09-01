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

	def parse_item(self, response):
		courses = response.xpath('//*[@id="courseinventorycontainer"]/div/div')
		units_regex = ur'\d+\s(-\s\d+)?' # regex for cases when `1 - 12 units` or `3 units`
		for c in courses:
			soup = BeautifulSoup(c.extract(), 'lxml')
			item = CatalogItem()
			dept, class_num = c.xpath('./p/a/span[1]/text()').extract()[0].split()
			item['dept'] = dept
			item['class_num'] = class_num
			item['title'] = c.xpath('./p/a/span[2]/text()').extract()[0]
			units_temp = c.xpath('./p/a/span[3]/text()').extract()[0]
			item['units'] = re.match(units_regex, units_temp).group(0).strip()
			item['details'] = ''.join(c.xpath('./div/p//text()').extract()).strip()
			item['prereqs'] = self.get_prereqs(c)
			item['course_level'] = self.get_course_level(c)
			item['cross_list'] = self.get_cross_list(c)
			yield item

	def get_prereqs(self, course, soup):
		prereqs_body = soup.body.findAll(text='Prerequisites:')
		if not prereqs_body:
			return ''
		return prereqs_body[0].next_element.strip()

	def get_course_level(self, course, soup):
		course_level_body = soup.body.findAll(text='Subject/Course Level:')
		if not course_level_body:
			return '' #shouldn't happen
		return course_level_body[0].next_element.strip().split('/')[-1]

	def get_cross_list(self, course, soup):
		cross_list_body = soup.body.findAll(text='Also listed as:')
		if not cross_list_body:
			return ''
		return cross_list_body[0].next_element.strip()