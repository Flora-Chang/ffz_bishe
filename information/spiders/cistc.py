# -*- coding: utf-8 -*-
import re
import scrapy
import json
from scrapy.http import Request
from information.items import InformationItem


class CistcSpider(scrapy.Spider):
    name = 'cistc'
    allowed_domains = ['cistc.gov.cn']
    start_urls = [
        #'http://www.cistc.gov.cn/handlers/cistcProjectInfoList.ashx?columnid=224&isall=1&keyword=&pagenum=1',  # 项目，项目公告
        #'http://www.cistc.gov.cn/handlers/cistcMenuInfoList.ashx?columnid=228&isall=1&keyword=&year=&pagenum=1',  # 项目，政府间科技合作项目
        # 'http://www.cistc.gov.cn/handlers/cistcProjectInfoList.ashx?columnid=229&isall=1&keyword=&pagenum=1',  # 项目，驻外科技机构推荐项目
        'http://www.cistc.gov.cn/handlers/cistcMenuInfoList.ashx?columnid=221&isall=1&keyword=&year=&pagenum=1',  # 科技部外事动态
            ]

    def parse(self, response):
        page_info = json.loads(response.body.decode("utf-8"))

        max_page = int(page_info.get('Maxpage'))
        page_num = int(page_info.get('Pagenum'))
        # project_list = page_info.get('Projectlist')

        print("max page: ", max_page)
        print("page num: ", page_num)
        column = re.findall(r'columnid=(\d+)', response.url)[0]
        print("url: ", response.url)
        print(column)
        tag_url = "http://www.cistc.gov.cn/handlers/cistcNavMenu.ashx?menuid={}".format(column)

        for i in range(1, max_page+1):
            print(i)
            list_url = 'http://www.cistc.gov.cn/handlers/cistcProjectInfoList.ashx?columnid=224&isall=1&keyword=&pagenum={}'.format(i)
            yield Request(list_url, callback=self.parse_list)

    def parse_list(self, response):
        print("parse_list ok")

        page_info = json.loads(response.body.decode("utf-8"))
        project_list = page_info.get('Projectlist')
        for project in project_list:
            tail_url = str(project.get('ProjectUrl'))
            column, infoid = re.findall(r'column=(\d+)&id=(\d+)', tail_url)[0]

            new_url = "http://www.cistc.gov.cn/handlers/cistcProjectInfo.ashx?infoid={}&contentLenth=&column={}" \
                .format(infoid, column)
            yield Request(new_url, callback=self.parse_article)

    # def parse_tags(self, response):
    #     menus = json.loads(response.body.decode('utf-8'))
    #     tags = []
    #     for item in menus.get('menus'):
    #         tags.append(item.get('MenuName'))
    #
    #
    #     yield Request(response.meta['article_url'], callback=self.parse_article, meta={'tags': tags})

    def parse_article(self, response):
        body = json.loads(response.body.decode('utf-8'))

        article = re.sub(r'</*.+?>', ' ', body.get('ProjectContent'))
        article = re.sub(r'[\xa0, \u3000, \t, &nbsp;]+', ' ', article.replace('\n', ' ').strip())
        post = InformationItem()

        post['title'] = body.get('ProjectTitle')
        post['publish_time'] = body.get('ProjectPublicDate').replace('/', '-')
        post['article'] = article.strip()
        post['tags'] =  ['科技部外事动态']
        post['url'] = response.url
        yield post