# -*- coding: utf-8 -*-
import re
import scrapy
import json
from scrapy.http import Request
from information.items import InformationItem


class NpdNsfcSpider(scrapy.Spider):
    name = 'npd_nsfc'
    allowed_domains = ['npd.nsfc.gov.cn']
    start_urls = ['http://npd.nsfc.gov.cn/areadropdet.action?areaCode=A01&page=1&sort=undefined',   # 数理科学部->数学
                  # 'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=A02&page=1&sort=undefined',   # 力学
                  # 'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=A03&page=1&sort=undefined',   # 天文学
                  # 'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=A04&page=1&sort=undefined',   # 物理学1
                  # 'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=A05&page=1&sort=undefined',    # 物理学2
                  # 'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=F01&page=1&sort=0',   # 信息科学部->通讯与电子学
                  # 'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=F02&page=1&sort=0',   # 信息科学部->计算机网络
                  # 'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=F03&page=1&sort=0',   # 信息科学部->控制理论
                  # 'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=F04&page=1&sort=0',   # 信息科学部->半导体科学与信息器件
                  ]

    def parse(self, response):
        max_page = response.xpath('//*[@id="page"]/font[2]/text()').extract()[0]
        max_page = int(re.findall(r'\d+', max_page)[0])
        base_url = response.url
        for i in range(1, max_page+1):
            new_url = re.sub(r'page=\d+&', 'page={}&'.format(i), base_url)
            print(new_url)
            print("*"*20)
            yield Request(new_url, callback=self.parse_list)
            break

    def parse_list(self, response):
        base_url = "npd.nsfc.gov.cn/"
        url_list = response.xpath('//*[@id="right"]/div/div/ul/li/dl/dt/a/@href').extract()
        for url in url_list:
            article_url = base_url + url
            print(article_url)
            print("#"*20)
            yield Request(article_url, callback=self.parse_article)
            break



    def parse_article(self, response):
        print(response.url)
        # title = response.xpath('//*[@id="right"]/h2/text()').extract()
        # zhaiyao = response.xpath('//*[@id="right"]/div/div[2]/p/text()').extract()
        # keyword = response.xpath('//*[@id="right"]/div/p/text()').extract()
        # url = response.url
        # time = response.xpath('//*[@id="right"]/p[8]/text()').extract()
        # danwei = response.xpath('//*[@id="right"]/p[7]/a/text()').extract()
        # author = response.xpath('//*[@id="right"]/p[5]/a/text()').extract()
        # tags = response.xpath('//*[@id="right"]/p[3]/text()').extract()
        # print("title: ", title)
        # print("zhaiyao: ", zhaiyao)
        # print("keyword: ", keyword)
        # print("url: ", url)
        # print("time: ", time)
        # print("danwei: ", danwei)
        # print("author: ", author)
        # print("tags: ", tags)



