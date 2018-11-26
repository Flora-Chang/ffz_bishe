# -*- coding: utf-8 -*-
import re
import scrapy
import json
import random
import time
from scrapy.http import Request
from information.items import InformationItem


class NpdNsfcSpider(scrapy.Spider):
    name = 'npd_nsfc'
    allowed_domains = ['npd.nsfc.gov.cn']
    start_urls = [
                # 'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=A01&page=1&sort=undefined',   # 1. 数理科学部->数学
                #   'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=A02&page=1&sort=undefined',   # 2. 力学
                #   'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=A03&page=1&sort=undefined',   # 3. 天文学
                  # 'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=A04&page=1&sort=undefined',   # 4. 物理学1
                  # 'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=A05&page=1&sort=undefined',    # 5.  物理学2
                  # 'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=F01&page=1&sort=0',   # 6. 信息科学部->通讯与电子学
                  # 'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=F02&page=1&sort=0',   # 7. 信息科学部->计算机网络
                  # 'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=F03&page=1&sort=0',   # 8. 信息科学部->控制理论
                  # 'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=F04&page=1&sort=0',   # 9. 信息科学部->半导体科学与信息器件
                  #   'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=C01&page=1&sort=0',   # 10. 生命科学部-> 微生物学
                  #   'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=C02&page=1&sort=0',   # 11. 生命科学部 -> 植物学
                  #   'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=C03&page=1&sort=0',     # 12
                  #   'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=C04&page=1&sort=0',   # 12
                  #   'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=C05&page=1&sort=0',   # 12
                  #   'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=C06&page=1&sort=0',  # 13
                  #   'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=C07&page=1&sort=0',  # 14
                  #   'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=C08&page=1&sort=0',  # 15
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=C09&page=1&sort=0',  # 16
                  ]

    def parse(self, response):
        # '//*[@id="right"]/div/div/ul/li[1]/dl/dt/a'
        # '//*[@id="right"]/div/div/ul/li[3]/dl/dt/a'
        # '//*[@id="page"]/font[2]'
        max_page = response.xpath('//*[@id="page"]/font[2]/text()').extract()[0]
        max_page = int(re.findall(r'\d+', max_page)[0])
        print("max page: ", max_page)

        base_url = response.url
        for i in range(2, max_page+1):
            time.sleep(random.randint(1, 10))
            new_url = re.sub(r'page=\d+&', 'page={}&'.format(i), base_url)
            print(new_url)
            print("*"*20)
            user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            yield Request(new_url, callback=self.parse_list)


    def parse_list(self, response):
        # print(response._body.decode('utf-8'))
        # print('-' * 80)
        base_url = "http://npd.nsfc.gov.cn/"
        url_list = response.xpath('//*[@id="right"]/div/div/ul/li/dl/dt/a/@href').extract()
        print(url_list)
        for url in url_list:
            article_url = base_url + url
            print(article_url)
            print("#"*20)
            user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0"
            yield Request(article_url, callback=self.parse_article)


    def parse_article(self, response):
        # print(response.url)
        # title = response.xpath('//*[@class="title"]/text()').extract()
        # zhaiyao = response.xpath('//*[@class="zyao"]/div/p/text()').extract()  # [中文摘要、英文摘要、结题摘要]
        # keyword = response.xpath('//*[@class="xmu"]/text()').extract()
        # print(title)
        # print(zhaiyao)
        # print(keyword)
        # print('-' * 80)
        title = response.xpath('//*[@id="right"]/h2/text()').extract()[0]
        zhaiyao = response.xpath('//*[@id="right"]/div/div[2]/p/text()').extract()[0]
        keyword = response.xpath('//*[@id="right"]/div/p/text()').extract()[0].split("；")
        time = response.xpath('//*[@id="right"]/p[8]/text()').extract()[0]
        danwei = response.xpath('//*[@id="right"]/p[7]/a/text()').extract()[0]
        author = response.xpath('//*[@id="right"]/p[5]/a/text()').extract()[0]
        tags = response.xpath('//*[@id="right"]/p[3]/text()').extract()
        # print("title: ", title)
        # print("zhaiyao: ", zhaiyao)
        # print("keyword: ", keyword)
        # print("time: ", time)
        # print("danwei: ", danwei)
        # print("author: ", author)
        # print("tags: ", tags)
        post = InformationItem()

        post['title'] = title
        post['publish_time'] = time
        post['article'] = zhaiyao
        post['tags'] = tags
        post['url'] = response.url
        post['author'] = author
        post['author_danwei'] = danwei
        post['keyword'] =keyword
        yield post



