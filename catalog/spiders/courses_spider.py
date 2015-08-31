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
			item = CatalogItem()
			item['code'] = c.xpath('./p/a/span[1]/text()').extract()
			item['title'] = c.xpath('./p/a/span[2]/text()').extract()[0]
			units_temp = c.xpath('./p/a/span[3]/text()').extract()[0]
			item['units'] = re.match(units_regex, units_temp).group(0).strip()
			item['details'] = ''.join(c.xpath('./div/p//text()').extract()).strip()
			item['prereqs'] = self.get_prereqs(c)
			yield item

	def get_prereqs(self, course):
		soup = BeautifulSoup(course.extract(), 'lxml')
		prereqs_body = soup.body.findAll(text='Prerequisites:')
		if not prereqs_body:
			return ''
		return prereqs_body[0].next_element.strip()