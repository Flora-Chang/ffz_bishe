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
                  #   'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=C09&page=1&sort=0',  # 16

                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=B01&page=1&sort=0',   # b01 化学科学部 -> 无机化学
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=B02&page=1&sort=0',  # b02 化学科学部 -> 有机化学
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=B03&page=1&sort=0',  # b03 化学科学部 -> 物理化学
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=B04&page=1&sort=0',  # b04 化学科学部 -> 高分子科学
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=B05&page=1&sort=0',  # b05 化学科学部 -> 分析化学
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=B06&page=1&sort=0',  # b06 化学科学部 -> 化学工程及工业化
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=B07&page=1&sort=0',  # b07 化学科学部 -> 环境化学

                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=D00&page=1&sort=0',  # d00 地球科学部 -> 综合与战略规划处
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=D01&page=1&sort=0',   # d01 地球科学部 -> 地理学
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=D02&page=1&sort=0',  # d02 地球科学部 -> 地质学
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=D03&page=1&sort=0',  # d03 地球科学部 -> 地球化学
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=D04&page=1&sort=0',  # d04 地球科学部 -> 地球物理学和空间物理学
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=D05&page=1&sort=0',  # d05 地球科学部 -> 大气科学
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=D06&page=1&sort=0',  # d06 地球科学部 -> 海洋科学

                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=E01&page=1&sort=0',   #  e01  工程与材料科学部-> 金属材料学科
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=E02&page=1&sort=0' ,   # e02  工程与材料科学部-> 无机非金属材料学科
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=E03&page=1&sort=0', # e03  工程与材料科学部-> 有机高分子材料学科
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=E04&page=1&sort=0',  # e04  工程与材料科学部-> 冶金与矿业学科
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=E05&page=1&sort=0',  # e05  工程与材料科学部-> 机械工程学科
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=E06&page=1&sort=0',  # e06  工程与材料科学部-> 工程物理与能源利用学科
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=E07&page=1&sort=0',  # e07  工程与材料科学部-> 电气科学与工程学科
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=E08&page=1&sort=0',  # e08  工程与材料科学部-> 建筑环境与结构工程学科
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=E09&page=1&sort=0',  # e09  工程与材料科学部-> 水里科学与海洋工程学科

                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H01&page=1&sort=0', # h01  医学科学部->呼吸系统
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H02&page=1&sort=0',  # h02
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H03&page=1&sort=0',  # h03
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H04&page=1&sort=0',  # h04
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H05&page=1&sort=0',  # h05
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H06&page=1&sort=0',  # h06
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H07&page=1&sort=0',  # h07
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H08&page=1&sort=0',  # h08
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H09&page=1&sort=0',  # h09
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H10&page=1&sort=0',  # h10
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H11&page=1&sort=0',  # h11
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H12&page=1&sort=0',  # h12
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H13&page=1&sort=0',  # h13
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H14&page=1&sort=0',  # h14
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H15&page=1&sort=0',  # h15
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H16&page=1&sort=0',  # h16
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H17&page=1&sort=0',  # h17
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H18&page=1&sort=0',  # h18
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H19&page=1&sort=0',  # h19
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H20&page=1&sort=0',  # h20
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H21&page=1&sort=0',  # h21
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H22&page=1&sort=0',  # h22
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H23&page=1&sort=0',  # h23
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H24&page=1&sort=0',  # h24
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H25&page=1&sort=0',  # h25
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H26&page=1&sort=0',  # h26
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H27&page=1&sort=0',  # h27
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H28&page=1&sort=0',  # h28
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H29&page=1&sort=0',  # h29
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H30&page=1&sort=0',  # h30
                    'http://npd.nsfc.gov.cn/areadropdet.action?areaCode=H31&page=1&sort=0',  # h31

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



