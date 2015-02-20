# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class LuaClass(scrapy.Item):
    name = scrapy.Field()
    ancestor = scrapy.Field()
    glob = scrapy.Field()
    glob_accessor = scrapy.Field()
    notes = scrapy.Field()
    methods = scrapy.Field()

class LuaMethod(scrapy.Item):
    name = scrapy.Field()
    signature = scrapy.Field()
    docs = scrapy.Field()
