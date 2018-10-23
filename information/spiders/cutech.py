# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from information.items import InformationItem


class CutechSpider(scrapy.Spider):
    name = 'cutech'
    allowed_domains = ['cutech.edu.cn']
    start_urls = [
        # 'http://www.cutech.edu.cn/cn/index.htm',

        'http://www.cutech.edu.cn/cn/sygd/A0137index_1.htm',  # 公告
        'http://www.cutech.edu.cn/cn/zxgz/A0136index_1.htm',  # 中心工作动态
        'http://www.cutech.edu.cn/cn/rxcz/A0127index_1.htm',  # 要闻咨讯
        'http://www.cutech.edu.cn/cn/Fund/A0159index_1.htm',  # 基金项目
        'http://www.cutech.edu.cn/cn/gxkj/A0128index_1.htm',  # 高校科技动态
        'http://www.cutech.edu.cn/cn/gwkj/A0129index_1.htm',  # 国际科技动态
        'http://www.cutech.edu.cn/cn/qslt/A0108index_1.htm',  # 学术评论
        'http://www.cutech.edu.cn/cn/zscq/A0113index_1.htm',  # 知识产权
        'http://www.cutech.edu.cn/cn/dxkj/A0118index_1.htm',  # 大学科技园

        'http://www.cutech.edu.cn/cn/zcfg/A0102index_1.htm',  # 政策法规
        'http://www.cutech.edu.cn/cn/dxph/A0121index_1.htm',  # 大学排行榜
        'http://www.cutech.edu.cn/cn/kyjj/A0103index_1.htm',  # 科研基金
        'http://www.cutech.edu.cn/cn/kjjl/A0106index_1.htm',  # 科技奖励
        'http://www.cutech.edu.cn/cn/kjcg/A0104index_1.htm',  # 科技成果
        'http://www.cutech.edu.cn/cn/cxyhz/A0157index_1.htm',  # 产学研合作
        'http://www.cutech.edu.cn/cn/kjcyh/A0166index_1.htm',  # 科技产业化
        'http://www.cutech.edu.cn/cn/jlrz/A0130index_1.htm',  # 计量认证
        'http://www.cutech.edu.cn/cn/jyxxh/A0109index_1.htm',  # 教育信息化
    ]

    def parse(self, response):
        base_url = 'http://www.cutech.edu.cn'
        try:
            urls = response.xpath('//*[@title="更多"]/@href').extract()
            for url in urls:
                new_url = base_url + url
                yield Request(new_url, callback=self.parse_list)
        except Exception:
            yield Request(response.url, callback=self.parse_list)

    def parse_list(self, response):
        def clean_list(l):
            res = []
            for item in l:
                item = re.sub(r'</*.+?>', ' ', item)
                item = re.sub(r'[\xa0, \u3000, \t]+', ' ', item.replace('\n', ' ').strip())
                if len(item) > 0:
                    res.append(item)
            return res

        base_url = 'http://www.cutech.edu.cn'
        urls = response.xpath('//*[@class="pagelist"]/tbody/tr/td/a/@href').extract()
        # print(urls)
        for url in urls:
            new_url = base_url + url
            yield Request(new_url, callback=self.parse_article)

        try:
            pages = response.xpath('//*[@class="fyinfo"]/a/text()').extract()
            page_lists = response.xpath('//*[@class="fyinfo"]/a/@href').extract()
            pages_info = dict(zip(clean_list(pages), page_lists))

            if '下一页' in pages_info:
                yield Request(base_url + pages_info['下一页'], callback=self.parse_list)
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

        title = response.xpath('//*[@class="ctitle"]/tbody/tr/td/text()').extract()
        publish_time = response.xpath('//*[@class="date"]/text()').extract()
        # article_data = response.xpath('//*[@id="BodyLabel"]')[0]
        # article = article_data.xpath('string(.)').extract()
        # print(len(article))
        # article = article[0].replace("\n", "").replace("\s+", " ").replace("\r", "")
        article = response.xpath('//*[@id="BodyLabel"]/p/text()').extract()
        if len(article) == 0:
            article = response.xpath('//*[@id="BodyLabel"]/text()').extract()
        tags = response.xpath('//*[@class="channelLink"]/text()').extract()

        title = ' '.join(clean_list(title))
        publish_time = ' '.join(re.findall(r'(\d{4}-\d{2}-\d{2})', ' '.join(clean_list(publish_time))))
        article = ' '.join(clean_list(article)).replace("\r", "")

        post = InformationItem()
        post['title'] = title
        post['publish_time'] = publish_time
        post['article'] = article
        post['tags'] = tags
        post['url'] = response.url

        yield post