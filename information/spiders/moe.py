# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from information.items import InformationItem
import time

class MoeSpider(scrapy.Spider):
    name = 'moe'
    allowed_domains = ['www.moe.edu.cn']
    start_urls = ['http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/index.html']

    def parse(self, response):
        print(response)
        for i in range(1, 10):
            print(i)
            new_url = 'http://www.moe.gov.cn/was5/web/search?page={}&channelid=282726&searchword=chnlid%3D2147438998&keyword=chnlid%3D2147438998&orderby=-DOCRELTIME&token=32.1423449772395.33&perpage=20&outlinepage=10&searchscope=&timescope=&timescopecolumn=&orderby=-DOCRELTIME&towcmurl=&andsen=&total=&orsen=&exclude='.format(i)
            print(new_url)
            yield Request(new_url, callback=self.parse_list)

    def parse_list(self, response):
        print(response)
        # projects_lists = response.xpath('//*[@id="wcmpagehtml"]/div[@class="scy_tylb-nr"]/ul/li/a/@href').extract()
        # print(projects_lists)

