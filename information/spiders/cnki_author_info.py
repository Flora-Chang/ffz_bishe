# -*- coding: utf-8 -*-
import time
import json
import scrapy
from scrapy.http import Request


class CnkiAuthorInfoSpider(scrapy.Spider):
    name = 'cnki_author_info'
    allowed_domains = ['cnki.net']

    def __init__(self, url=None, *args, **kwargs):
        super(CnkiAuthorInfoSpider, self).__init__(*args, **kwargs)
        self.url = json.loads(url)['url']

    def start_requests(self):
        # 1、使用姓名和单位检索（POST）; 2、使用返回的cookie去get结果即可。
        # url = 'http://kns.cnki.net/kns/request/SearchHandler.ashx'
        #
        # formdata = {
        #     'action': '',
        #     'NaviCode': '*',
        #     'ua': '1.21',
        #     'isinEn': '1',
        #     'PageName': 'ASP.brief_result_aspx',
        #     'DbPrefix': 'SCDB',
        #     'DbCatalog': '中国学术文献网络出版总库',
        #     'ConfigFile': 'SCDB.xml',
        #     'db_opt': 'CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
        #     'au_1_sel': 'AU',
        #     'au_1_sel2': 'AF',
        #     'au_1_value1': '周昌令',
        #     'au_1_value2': '北京大学',
        #     'au_1_special1': '%',
        #     'au_1_special2': '%',
        #     'his': '0',
        #     '__': '{} GMT+0800 (中国标准时间)'.format(time.strftime("%a %b %d %Y %H:%M:%S", time.localtime())),
        # }
        #
        # cookie = 'Ecp_ClientId=4181203190702387619; UM_distinctid=16773c08bf2617-073c38f3ffa235-3d740c5e-1fa400-16773c08bf3121f; Ecp_IpLoginFail=181215111.202.192.3; ASP.NET_SessionId=lrjw4gaufyffpzlfvfdzmbq0; SID_kns=123114; SID_klogin=125142; ASPSESSIONIDQSSBATBC=PGHJBPLBHDJLMOPDFGIJLHHD; KNS_SortType=; RsPerPage=20; SID_krsnew=125133; cnkiUserKey=92eb3dfa-62de-0145-a6a0-9d5ed32636ab; SID_kxreader_new=011121; SID_kcms=124102; _pk_ref=%5B%22%22%2C%22%22%2C1544874781%2C%22http%3A%2F%2Fwww.cnki.net%2F%22%5D; _pk_ses=*'
        # headers = {
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #     'Accept-Encoding': 'gzip, deflate',
        #     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,lv;q=0.7,zh-TW;q=0.6',
        #     'Connection': 'keep-alive',
        #     'Host': 'nvsm.cnki.net',
        #     'Referer': 'http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB&crossDbcodes=CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
        #     'Upgrade-Insecure-Requests': 1,
        #     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Mobile Safari/537.36'
        # }
        # headers['Cookie'] = cookie
        #
        # yield scrapy.FormRequest(
        #     url=url,
        #     formdata=formdata,
        #     callback=self.parse,
        #     headers=headers,
        #     meta={'headers': headers, 'queryID': 1}
        # )
        print("url: ", self.url)
        yield Request(url=self.url, callback=self.parse_basic_info)

    def parse(self, response):
        yield Request(url=self.url, callback=self.parse_basic_info, headers=response.meta['headers'],
                      meta=response.meta)

    def parse_basic_info(self, response):
        name = response.xpath('//*[@class="name"]/text()').extract()
        print("name: ", name)

        orgn = response.xpath('//*[@class="info"]/p/a/text()').extract()
        print("orgn: ", orgn)

        doma = response.xpath('//*[@class="info"]/p[2]/text()').extract()
        print("doma: ", doma)

        num = response.xpath('//*[@class="info"]/p[3]/span/text()').extract()

        print("num: ", num)
