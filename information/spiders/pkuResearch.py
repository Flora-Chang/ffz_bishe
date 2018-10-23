# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from information.items import InformationItem


class PkuResearchSpider(scrapy.Spider):
    name = 'pkuResearch'
    allowed_domains = ['research.pku.edu.cn']
    start_urls = [
        'http://www.research.pku.edu.cn/bdkyjz/index.htm',  # 北大科研进展，翻页
        'http://www.research.pku.edu.cn/gnwkydt/index.htm',  # 国内外科研动态
        'http://www.research.pku.edu.cn/tzgg/index.htm',  # 通知公告，翻页
        'http://www.research.pku.edu.cn/kyxm/index.htm',  # 科研项目
        'http://www.research.pku.edu.cn/kyjd/tzggj/index.htm',  # 科研基地,基地通知公告
        'http://www.research.pku.edu.cn/kyjd/cyljj/index.htm',  # 科研基地,政策
        'http://www.research.pku.edu.cn/kycg/kyjl/index.htm',  # 科研成果，科研奖励
        'http://www.research.pku.edu.cn/kycg/zscq/index.htm',  # 科研成果，知识产权
        'http://www.research.pku.edu.cn/kycg/kjlw/index.htm',  # 科研成果，科技论文
        'http://www.research.pku.edu.cn/gjhzyjl/gjkjhz/index.htm',  # 国际合作与交流，国际科技合作
        'http://www.research.pku.edu.cn/gjhzyjl/gjxzjl/index.htm',   # 国际合作与交流，国际学术交流
        'http://www.research.pku.edu.cn/xxgkgs/index.htm'  # 信息公告
    ]

    def parse(self, response):
        print(response.url)
        base_url = response.url.rsplit('/', 1)[0]
        urls = response.xpath('//*[@class="list03"]/li/a/@href').extract()

        for url in urls:
            new_url = base_url + '/' + url
            # print(new_url)
            yield Request(new_url, callback=self.parse_article)

        try:
            next_page = response.xpath('//*[@class="page"]/div/a[3]/@href').extract()[0]
            last_page = response.xpath('//*[@class="page"]/div/a[4]/@href').extract()[0]
            if next_page != last_page:
                url = base_url + '/' + next_page
                yield Request(url, callback=self.parse)
        except Exception:
            pass

    def parse_article(self, response):
        def clean_list(l):
            res = []
            for item in l:
                item = re.sub(r'</*.+?>', ' ', item)
                item = re.sub(r'[\xa0, \u3000, \t]+', ' ', item.replace('\n', ' ').strip())
                if len(item) > 0:
                    res.append(item)
            return res

        title = response.xpath('//*[@class="articleTitle"]/h3/text()').extract()
        publish_time = response.xpath('//*[@class="articleAuthor"]/text()').extract()
        article = response.xpath('//*[@class="article"]').extract()

        tags = response.xpath('//*[@class="bread"]').extract()

        title = ' '.join(clean_list(title))
        publish_time = ' '.join(clean_list(publish_time))
        article = ' '.join(clean_list(article))
        tags = clean_list(tags)[0].split(' »\r ')[1:]

        post = InformationItem()
        post['title'] = title
        post['publish_time'] = publish_time
        post['article'] = article
        post['tags'] = tags
        post['url'] = response.url
        yield post