# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from information.items import InformationItem


class CistcSpider(scrapy.Spider):
    name = 'cistc'
    allowed_domains = ['www.cistc.gov.cn']
    start_urls = [
        #'http://http://www.cistc.gov.cn//',

    ]

    def parse(self, response):
        pass
