# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from information.items import InformationItem
import re

class NsfcSpider(scrapy.Spider):
    name = 'nsfc'
    allowed_domains = ['nsfc.gov.cn']
    start_urls = ['http://www.nsfc.gov.cn/publish/portal0/tab434/module1146/more.htm',
                  'http://www.nsfc.gov.cn/publish/portal0/tab448/',
                  'http://www.nsfc.gov.cn/publish/portal0/tab446/',
                  'http://www.nsfc.gov.cn/publish/portal0/tab440/'
                    ]

    def parse(self, response):
        href_list = response.xpath('//a[@class="Normal"]/@href').extract()
        print('href_list: ', href_list)
        max_page = int(re.findall(r'\d+',href_list[-1].split('/')[-1])[0])
        for i in range(1, max_page+1):
            if response.url == 'http://www.nsfc.gov.cn/publish/portal0/tab434/module1146/more.htm':
                new_url = 'http://www.nsfc.gov.cn/publish/portal0/tab442/module1178/page{}.htm'.format(i)
            elif response.url == 'http://www.nsfc.gov.cn/publish/portal0/tab448/':
                new_url = 'http://www.nsfc.gov.cn/publish/portal0/tab448/module1190/page{}.htm'.format(i)
            elif response.url == 'http://www.nsfc.gov.cn/publish/portal0/tab446/':
                new_url = 'http://www.nsfc.gov.cn/publish/portal0/tab446/module1185/page{}.htm'.format(i)
            elif response.url == 'http://www.nsfc.gov.cn/publish/portal0/tab440/':
                new_url = 'http://www.nsfc.gov.cn/publish/portal0/tab440/module1176/page{}.htm'.format(i)

            yield Request(new_url, callback=self.parse_list)



    def parse_list(self, response):
        base_url = 'http://www.nsfc.gov.cn'
        project_list = response.xpath('//*[@class="fl"]/a/@href').extract()
        for url in project_list:
            new_url = base_url + url
            yield Request(new_url, callback=self.parse_article)

    def parse_article(self, response):
        publish_time = response.xpath('//*[@class="line_xilan"]/text()').extract()
        publish_time = ' '.join(re.findall(r'(\d{4}-\d{2}-\d{2})', ' '.join(publish_time)))
        title = response.xpath('//*[@class="title_xilan"]/h1/text()').extract()
        tags = response.xpath('//*[@id="ess_essBREADCRUMB_lblBreadCrumb"]/a/text()').extract()[1:]
        article = response.xpath('//*[@id="zoom"]/p/text()').extract()
        if len(article) >= 8:
            article = article[:-6]
        article = " ".join(article).replace("\t", " ").replace("\n", " ").replace(" ", "")
        print("public_time: ", publish_time)
        print("title:", title)
        print("tags: ", tags)
        print("article: ", article)
        post = InformationItem()
        post['title'] = title
        post['publish_time'] = publish_time
        post['article'] = article
        post['tags'] = tags
        post['url'] = response.url
        yield post








