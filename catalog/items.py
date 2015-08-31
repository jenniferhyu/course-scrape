# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class CatalogItem(Item):
    code = Field()
    title = Field()
    units = Field()
    details = Field()
    prereqs = Field()
    course_level = Field()
    cross_list = Field()