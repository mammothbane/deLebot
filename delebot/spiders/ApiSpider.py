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
        ancSibs = ancestors.xpath("preceding::h3[1]/span//text()").extract()
        clist = []
        for clss in classes:
            lClass = LuaClass()
            lClass['glob'] = False
            lClass['glob_accessor'] = ""
            lClass['name'] = self.pretty_print(clss.xpath("preceding-sibling::h3[1]/span//text()").extract())
            if lClass['name'] == 'Global':
                lClass['glob'] = True
            notes = self.pretty_print(clss.xpath("preceding-sibling::p[1]//text()").extract())
            if "Global" in notes: #this class has a global accessor
                notes = self.pretty_print(clss.xpath("preceding-sibling::p[2]//text()").extract())
                lClass['glob'] = True
                lClass['glob_accessor'] = self.pretty_print(clss.xpath("preceding-sibling::p[1]/code//text()").extract())
            glob_accessor = self.pretty_print(clss.xpath("preceding-sibling::code[1]//text()").extract())
            if notes != "No Description Set":
                lClass['notes'] = notes
            lClass['methods'] = []
            for i in range(0, len(ancSibs)):
                if self.pretty_print(ancSibs[i]) == lClass['name']:
                    lClass['ancestor'] = self.pretty_print(ancestors[i].xpath(".//text()").extract())
                    break
            xMethods = clss.xpath("./tr")
            for xMethod in xMethods:
                name = self.pretty_print(xMethod.xpath("./td[1]/a//text()").extract())
                if name == "":
                    continue
                method = LuaMethod()
                method['name'] = name
                method['signature'] = self.pretty_print(xMethod.xpath(".//code//text()").extract())
                docs = self.pretty_print((xMethod.xpath("./td[3]//text()").extract())).split(':')
                method['docs'] = ''
                if len(docs) > 1:
                    for i in range(1, len(docs) - 1):
                        method['docs'] = method['docs'].join(docs[i])
                else:
                    method['docs'] = docs[0]
                lClass['methods'].append(method)
            clist.append(lClass)

        self.construct_stubs(clist)
        return clist

    def pretty_print(self, str):
        if len(str) > 0:
            return BeautifulSoup(''.join(str)).get_text().strip()
        else:
            return ""

    def construct_stubs(self, list):
        if not os.path.exists("stubs"):
            os.makedirs("stubs")
        for lClass in list:
            self.writeStubFile(lClass['name'], lClass['glob'], lClass['methods'])
            if lClass['glob'] and lClass['glob_accessor'] != "":
                self.writeStubFile(lClass['glob_accessor'], False, lClass['methods'])

    def writeStubFile(self, name, glob, methods):
        fname = 'stubs/'+name+'.lua'
        with codecs.open(fname, 'w+', 'utf-8') as f:
            if not glob:
                f.write(name + ' = {}\n\n')
            for method in methods:
                f.write('--[[\n' + method['docs'] + '\nParams: ' + '\n' + ']]\n')
                f.write('function ' + ((name + ":") if not glob else "") + method['name'] + '(' + '' + ')\n')
                f.write('end\n\n')

    def parseSig(self, method):
        pass