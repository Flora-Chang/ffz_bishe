# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from information.items import InformationItem


class CistcSpider(scrapy.Spider):
    name = 'cistc'
    allowed_domains = ['cistc.gov.cn']
    start_urls = [
        'http://www.cistc.gov.cn/Project_Center_2.html?column=224'
        #'http://http://www.cistc.gov.cn//',
        #'http: // www.cistc.gov.cn/info_2.html?column=221',
        # 'http://www.cistc.gov.cn/info_2.html?column=764',
        # 'http://www.cistc.gov.cn/info_2.html?column=223',
        # 'http://www.cistc.gov.cn/info_2.html?column=344',
        # 'http://www.cistc.gov.cn/Project_Center_2.html?column=224',
        # 'http://www.cistc.gov.cn/info_2.html?column=222'

    ]

    def parse(self, response):
        # base_url = "http://www.cistc.gov.cn/"
        print(response)
        page_nums = response.xpath('//*[@id="infolist"]/li/a/@href').extract()
        print(page_nums)

    def parse_lsit(self, response):
        pass

    def parse_article(self, response):
        pass
