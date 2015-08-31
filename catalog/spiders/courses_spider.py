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
		soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
		course_body = soup.find_all('div', class_="coursedetails")
		units_regex = ur'\d+\s(-\s\d+)?' # regex for cases when `1 - 12 units` or `3 units`
		for c, c_info in zip(courses, course_body):
			item = CatalogItem()
			item['code'] = c.xpath('./p/a/span[1]/text()').extract()
			item['title'] = c.xpath('./p/a/span[2]/text()').extract()[0]
			units_temp = c.xpath('./p/a/span[3]/text()').extract()[0]
			item['units'] = re.match(units_regex, units_temp).group(0).strip()
			item['details'] = ''.join(c.xpath('./div/p//text()').extract()).strip()
			item['prereqs'] = c_info.text # needs better formatting but we have found the workaround!
			yield item
