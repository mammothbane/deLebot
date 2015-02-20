from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import scrapy

__author__ = 'mammothbane'

class LuaClass(scrapy.Item):
    name = scrapy.Field
    ancestor = scrapy.Field
    notes = scrapy.Field
    pass

class LuaMethod(scrapy.Item):
    name = scrapy.Field
    signature = scrapy.Field
    docs = scrapy.Field
    pass

class ApiSpider(CrawlSpider):

    name = 'api'
    allowed_domains = ['valvesoftware.com']
    start_urls = ['https://developer.valvesoftware.com/wiki/Dota_2_Workshop_Tools/Scripting/API']
    rules = [Rule()]

    def parse_api(self, response):
        l = LuaClass()
