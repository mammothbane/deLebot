from scrapy.contrib.spiders import CrawlSpider
from delebot.items import LuaClass, LuaMethod

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
            lClass['name'] = str(clss.xpath("preceding-sibling::h3[1]/span/text()").extract()).strip('u\'[] \n')
            notes = str(clss.xpath("preceding-sibling::p[1]/i/text()").extract()).strip('u\'[] \n')
            if notes != "No Description Set":
                lClass['notes'] = notes
            lClass['methods'] = []
            for i in range(0, len(ancSibs)):
                if str(ancSibs[i]).strip('u\'[] \n') == lClass['name']:
                    lClass['ancestor'] = str(ancestors[i].xpath("text()").extract()).strip('u\'[] \n')
                    break
            xMethods = clss.xpath("./tr")
            for xMethod in xMethods:
                method = LuaMethod()
                method['name'] = str(xMethod.xpath("./td[1]/a/text()").extract()).strip('u\'[] \n')
                method['signature'] = str(xMethod.xpath(".//code/text()").extract()).strip('u\'[] \n')
                method['docs'] = str(xMethod.xpath("./td[3]/text()").extract()).strip('u\'[] \n')
                lClass['methods'].append(method)
            clist.append(lClass)
        return clist