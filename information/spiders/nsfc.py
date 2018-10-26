# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from information.items import InformationItem
import re

class NsfcSpider(scrapy.Spider):
    name = 'nsfc'
    allowed_domains = ['nsfc.gov.cn']
    start_urls = ['http://www.nsfc.gov.cn/publish/portal0/tab434/module1146/more.htm']

    def parse(self, response):
        href_list = response.xpath('//*[@id="ess_ctr1178_ListC_Info_AspNetPager"]/table/tr/td[1]/a/@href').extract()
        max_page = int(re.findall(r'\d+',href_list[-1].split('/')[-1])[0])
        print(max_page)
        for i in range(1, max_page+1):
            new_url = 'http://www.nsfc.gov.cn/publish/portal0/tab442/module1178/page{}.htm'.format(i)
            yield Request(new_url, callback=self.parse_list)
            break

    def parse_list(self, response):
        project_list = response.xpath('//*[@id="ess_ctr1178_ModuleContent"]/tbody/tr/td/ul/ul/li/span[2]/a/@href').extract()
        print(project_list)



