# -*- coding: utf-8 -*-
import os
import re
import time
import scrapy
import requests
from lxml import etree
from scrapy.http import Request
from information.items import Paper


class CnkiBuzhuaSpider(scrapy.Spider):
    name = 'cnki_buzhua'
    allowed_domains = ['cnki.net']
    start_urls = ['http://kns.cnki.net/kns/request/SearchHandler.ashx']

    def start_requests(self):
        # 1、使用姓名和单位检索（POST）; 2、使用返回的cookie去get结果即可。
        url = 'http://kns.cnki.net/kns/request/SearchHandler.ashx'

        formdata = {
            'action': '',
            'NaviCode': '*',
            'ua': '1.21',
            'isinEn': '1',
            'PageName': 'ASP.brief_result_aspx',
            'DbPrefix': 'SCDB',
            'DbCatalog': '中国学术文献网络出版总库',
            'ConfigFile': 'SCDB.xml',
            'db_opt': 'CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
            'au_1_sel': 'AU',
            'au_1_sel2': 'AF',
            'au_1_value1': '周昌令',
            'au_1_value2': '北京大学',
            'au_1_special1': '%',
            'au_1_special2': '%',
            'his': '0',
            '__': '{} GMT+0800 (中国标准时间)'.format(time.strftime("%a %b %d %Y %H:%M:%S", time.localtime())),
        }

        cookie = 'Ecp_ClientId=4181203190702387619; UM_distinctid=16773c08bf2617-073c38f3ffa235-3d740c5e-1fa400-16773c08bf3121f; Ecp_IpLoginFail=181215111.202.192.3; ASP.NET_SessionId=lrjw4gaufyffpzlfvfdzmbq0; SID_kns=123114; SID_klogin=125142; ASPSESSIONIDQSSBATBC=PGHJBPLBHDJLMOPDFGIJLHHD; KNS_SortType=; RsPerPage=20; SID_krsnew=125133; cnkiUserKey=92eb3dfa-62de-0145-a6a0-9d5ed32636ab; SID_kxreader_new=011121; SID_kcms=124102; _pk_ref=%5B%22%22%2C%22%22%2C1544874781%2C%22http%3A%2F%2Fwww.cnki.net%2F%22%5D; _pk_ses=*'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,lv;q=0.7,zh-TW;q=0.6',
            'Connection': 'keep-alive',
            'Host': 'nvsm.cnki.net',
            'Referer': 'http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB&crossDbcodes=CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Mobile Safari/537.36'
        }
        headers['Cookie'] = cookie

        yield scrapy.FormRequest(
            url=url,
            formdata=formdata,
            callback=self.parse,
            headers=headers,
            meta={'headers': headers, 'queryID': 1}
        )

    def parse(self, response):
        pwd = os.path.dirname(__file__)
        in_file = os.path.join(pwd, "../../resources/cnki.buzhua.txt")
        with open(in_file) as f:
            for url in f:
                yield Request(url=url, callback=self.parse_paper_info, headers=response.meta['headers'],
                              meta=response.meta)

    def parse_paper_info(self, response):
        base_url = 'http://kns.cnki.net'

        # print(response.text)
        title = response.xpath('//*[@class="title"]/text()').extract()[0]
        authors = response.xpath('//*[@class="author"]/span/a/text()').extract()
        author_orgs = response.xpath('//*[@class="orgn"]/span/a/text()').extract()
        author_orgs = ' '.join(author_orgs)
        abstract = response.xpath('//*[@id="ChDivSummary"]/text()').extract()
        if isinstance(abstract, list) and len(abstract) > 0:
            abstract = abstract[0]
        # _fund = response.xpath('//*[@id="catalog_FUND"]/ancestor::p/a/text()').extract()
        # fund = _fund.     # 处理多个拼接问题

        _keywords = response.xpath('//*[@id="catalog_KEYWORD"]/../a/text()').extract()
        keywords = [re.sub(r'[;\r\n +]+', '', k) for k in _keywords]
        class_nums = response.xpath('//*[@id="catalog_ZTCLS"]/../text()').extract()
        if isinstance(class_nums, list) and len(class_nums) > 0:
            class_nums = class_nums[0].split(";")

        note = response.xpath('//*[@class="btn-note"]/@href').extract()
        if isinstance(note, list) and len(note) > 0:
            note = note[0]

        db_info = re.findall(r'testlunbo\?(.*)&filesourcetype=1', note)
        if len(db_info) > 0:
            db_info = db_info[0]

        paper = Paper()
        paper['url'] = response.url

        paper['title'] = title
        paper['authors'] = authors
        paper['author_orgs'] = author_orgs
        paper['abstract'] = abstract
        paper['keywords'] = keywords
        paper['class_nums'] = class_nums

        # 参考文献
        try:
            reference_url = 'http://kns.cnki.net/kcms/detail/frame/list.aspx?{}&RefType=1&vl='.format(db_info)
            reference_response = requests.get(url=reference_url)
            references = etree.HTML(reference_response.text).xpath('//*[@target="kcmstarget"]')
            references = [(liter.text, base_url + liter.xpath('@href')[0]) for liter in references]
        except Exception as e:
            print("无法获取参考文献。", e)
            references = []

        paper['references'] = references

        # 相似文献
        try:
            similar_liter_url = 'http://kns.cnki.net/kcms/detail/frame/asynlist.aspx?{}&reftype=604' \
                                '&catalogId=lcatalog_func604&catalogName=%E7%9B%B8%E4%BC%BC%E6%96%87%E7%8C%AE%0A%20%20%20' \
                                '%20%20%20%20%20%20%20'.format(db_info)
            similar_response = requests.get(url=similar_liter_url)
            liters = etree.HTML(similar_response.text).xpath('//*[@target="kcmstarget"]')
            similar_liters = [(liter.text, base_url + liter.xpath('@href')[0]) for liter in liters]
        except Exception as e:
            print("无法获取相似文献。", e)
            similar_liters = []

        paper['similar_liters'] = similar_liters

        # 读者推荐
        try:
            reader_rec_url = 'http://kns.cnki.net/kcms/detail/frame/asynlist.aspx?{}&reftype=605&catalogId=lcatalog_func605' \
                             '&catalogName=%E8%AF%BB%E8%80%85%E6%8E%A8%E8%8D%90%0A%20%20%20%20%20%20%20%20%20%20'.format(db_info)
            reader_rec_response = requests.get(url=reader_rec_url)
            reader_recs = etree.HTML(reader_rec_response.text).xpath('//*[@target="kcmstarget"]')
            reader_recs = [(liter.text, base_url + liter.xpath('@href')[0]) for liter in reader_recs]
        except Exception as e:
            print("无法获取读者推荐。", e)
            reader_recs = []

        paper['reader_recs'] = reader_recs

        yield paper
