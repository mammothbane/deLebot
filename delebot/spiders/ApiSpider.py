from scrapy.contrib.spiders import CrawlSpider
from delebot.items import LuaClass, LuaMethod
import scrapy


__author__ = 'mammothbane'



class ApiSpider(CrawlSpider):

    name = 'api'
    allowed_domains = ['developer.valvesoftware.com']
    start_urls = ['https://developer.valvesoftware.com/wiki/Dota_2_Workshop_Tools/Scripting/API']

    def parse(self, response):
        classes = response.xpath("//span[@class='mw-headline']")
        for clz in classes:
            luaClass = LuaClass()
            nm = clz.xpath("text()").extract
            if nm:
                luaClass.name = nm


            clz.xpath()
