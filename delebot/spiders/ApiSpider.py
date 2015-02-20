from scrapy.contrib.spiders import CrawlSpider
from delebot.items import LuaClass, LuaMethod
from bs4 import BeautifulSoup
import codecs
import os

__author__ = 'mammothbane'


class ApiSpider(CrawlSpider):
    name = 'api'
    allowed_domains = ['developer.valvesoftware.com']
    start_urls = ['https://developer.valvesoftware.com/wiki/Dota_2_Workshop_Tools/Scripting/API']

    def parse(self, response):
        classes = response.xpath("//table[@class='standard-table']")
        ancestors = response.xpath("//dd/a")
        ancSibs = ancestors.xpath("preceding::h3[1]/span/text()").extract()
        clist = []
        for clss in classes:
            lClass = LuaClass()
            lClass['name'] = self.pretty_print(clss.xpath("preceding-sibling::h3[1]/span/text()").extract())
            notes = self.pretty_print(clss.xpath("preceding-sibling::p[1]/i/text()").extract())
            if notes != "No Description Set":
                lClass['notes'] = notes
            lClass['methods'] = []
            for i in range(0, len(ancSibs)):
                if self.pretty_print(ancSibs[i]) == lClass['name']:
                    lClass['ancestor'] = self.pretty_print(ancestors[i].xpath("text()").extract())
                    break
            xMethods = clss.xpath("./tr")
            for xMethod in xMethods:
                name = self.pretty_print(xMethod.xpath("./td[1]/a/text()").extract())
                if name == "":
                    continue
                method = LuaMethod()
                method['name'] = name
                method['signature'] = self.pretty_print(xMethod.xpath(".//code/text()").extract())
                method['docs'] = self.pretty_print(xMethod.xpath("./td[3]/text()").extract())
                lClass['methods'].append(method)
            clist.append(lClass)

        self.construct_stubs(clist)
        return clist

    def pretty_print(self, str):
        if len(str) > 0:
            return BeautifulSoup(str[0]).get_text().strip()
        else:
            return ""

    def construct_stubs(self, list):
        if not os.path.exists("stubs"):
            os.makedirs("stubs")
        for lClass in list:
            name = lClass['name']
            fname = 'stubs/'+name+'.lua'
            with codecs.open(fname, 'w+', 'utf-8') as f:
                f.write(name + ' = {}\n\n')
                for method in lClass['methods']:
                    f.write('--[[\n' + method['docs'] + '\nParams: ' + '\n' + ']]\n')
                    f.write('function ' + name + ":" + method['name'] + '(' + '' + ')\n')
                    f.write('end\n\n')


    def parseSig(self, method):
        pass