# -*- coding: utf-8 -*-
import scrapy
import json


class TreeRegistrySpider(scrapy.Spider):
    name = 'tree_registry'
    allowed_domains = ['http://www.greening.gov.hk/']
    lang = 'en-US'

    def start_requests(self):
        data = {'codeType': 'TreeCode', 'code': '', 'ts': '0', 'distID':0, 'departID':0,'tc':0,'brr':False, 'lang': self.lang}
        yield scrapy.Request('http://www.greening.gov.hk/treeregister/map/iTreeService.asmx/GetTreeBySearch', method='POST', body=json.dumps(data), headers={'Content-Type': 'application/json; charset=UTF-8'}, callback=self.parse_search_result, dont_filter=True)

    def parse_search_result(self, response):
        d = json.loads(response.body_as_unicode())['d']
        for item in d:
            data = {'id': item["ID"], 'lang': self.lang}
            yield scrapy.Request('http://www.greening.gov.hk/treeregister/map/iTreeService.asmx/GetTreeMapInfo', method='POST', body=json.dumps(data), headers={'Content-Type': 'application/json; charset=UTF-8'}, callback=self.parse_info_result, meta={'d': item}, dont_filter=True)  

    def parse_info_result(self, response):
        output = json.loads(response.body_as_unicode())['d']
        output.update(response.meta['d'])
        yield output
