# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from information.items import InformationItem
import time
import re
import random

class MoeSpider(scrapy.Spider):
    name = 'moe'
    allowed_domains = ['www.moe.gov.cn']
    start_urls = ['http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/index.html']

    def parse(self, response):
        base_url = "http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/"
        # print('url: ', response.url)

        page_num = 0
        urls_list = response.xpath('//*[@id="wcmpagehtml"]/div[1]/ul/li/a/@href').extract()

        while len(urls_list) > 0:
            time.sleep(random.randint(2, 5))
            print("len: ", len(urls_list))
            # print(len(urls_list))
            for url in urls_list:
                new_url = base_url + '/'.join(url.split('/')[1:])
                yield Request(new_url, callback=self.parse_article)

            page_num += 1
            url = 'http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/index_{}.html'.format(page_num)
            yield Request(url, callback=self.parse)

    def parse_article(self, response):
        article_list = response.xpath('//*[@class="TRS_Editor"]/p/text()').extract()
        article = " ".join(article_list)
        title = response.xpath('//*[@id="content_body"]/h1/text()').extract()[0]
        tags = response.xpath('//*[@id="curpage"]/a/text()').extract()[1:]
        publish_time = response.xpath('//*[@id="content_date_source"]/text()').extract()
        publish_time = ' '.join(re.findall(r'(\d{4}-\d{2}-\d{2})', ' '.join(publish_time)))

        post = InformationItem()
        post['title'] = title
        post['publish_time'] = publish_time
        post['article'] = article
        post['tags'] = tags
        post['url'] = response.url
        yield  post



