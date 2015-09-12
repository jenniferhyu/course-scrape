# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class CatalogItem(Item):
    dept = Field()
    full_dept = Field()
    class_num = Field()
    title = Field()
    units = Field()
    description = Field()
    prereqs = Field()
    course_level = Field()
    cross_list = Field()
    grading = Field()
    final_exam = Field()
    format = Field()
    previously = Field()
    fall = Field()
    spring = Field()
    credit_restriction = Field()
