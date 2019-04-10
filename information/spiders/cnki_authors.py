# -*- coding: utf-8 -*-
import os
import re
import json
import time
import scrapy
import requests
from urllib import parse

from scrapy.http import Request
from lxml import etree
from information.items import Author


author_code_pat = re.compile(r'(sdb=.*&scode=\d*);+')


class CnkiAuthorsSpider(scrapy.Spider):
    name = 'cnki_authors'
    allowed_domains = ['cnki.net']
    author = Author()

    def __init__(self, row=None, idx=0, *args, **kwargs):
        super(CnkiAuthorsSpider, self).__init__(*args, **kwargs)
        self.line = row
        self.idx = idx

    def start_requests(self):
        # 1、使用姓名和单位检索（POST）; 2、使用返回的cookie去get结果即可。
        url = 'http://nvsm.cnki.net/kns/request/SearchHandler.ashx'

        name = json.loads(self.line)['name'].replace(" ", "")
        print(self.idx, " ", name)
        self.idx += 1
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
            'au_1_value1': name,
            'au_1_value2': '北京大学',
            'au_1_special1': '%',
            'au_1_special2': '%',
            'his': '0',
            '__': '{} GMT+0800 (中国标准时间)'.format(time.strftime("%a %b %d %Y %H:%M:%S", time.localtime())),
        }

        cookie = 'Ecp_notFirstLogin=j12T2T; Ecp_ClientId=5190409202802305835; ASP.NET_SessionId=skifwugx1gy35d10zybpbpm2; SID_kns=011101; Ecp_session=1; SID=011109; KNS_SortType=; RsPerPage=20; cnkiUserKey=78d96128-646a-83eb-461a-9de3e54c591c; UM_distinctid=16a022b5efa50e-07d7fe1416a4df-3e7e045d-1fa400-16a022b5efb57a; LID=WEEvREcwSlJHSldRa1FhdXNXaEd2QTlad1pCWFYzR2llVUsxS0dsdzRmQT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!; Ecp_LoginStuts=%7B%22IsAutoLogin%22%3Afalse%2C%22UserName%22%3A%22K10001%22%2C%22ShowName%22%3A%22%25E5%258C%2597%25E4%25BA%25AC%25E5%25A4%25A7%25E5%25AD%25A6%25E5%259B%25BE%25E4%25B9%25A6%25E9%25A6%2586%22%2C%22UserType%22%3A%22bk%22%2C%22r%22%3A%22j12T2T%22%7D; c_m_LinID=LinID=WEEvREcwSlJHSldRa1FhdXNXaEd2QTlad1pCWFYzR2llVUsxS0dsdzRmQT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!&ot=04/09/2019 22:46:29; c_m_expire=2019-04-09 22:46:29; _pk_ref=%5B%22%22%2C%22%22%2C1554819991%2C%22http%3A%2F%2Fcnki.net%2F%22%5D; _pk_ses=*'
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
            callback=self.get_search_result_page,
            headers=headers,
            meta={'headers': headers, 'queryID': self.idx}
        )

    def get_search_result_page(self, response):
        # 先 POST 再 GET
        # print('headers: ', response.headers)
        # cookie_list = response.headers.getlist('Set-Cookie')
        # cookie = b''.join(cookie_list).decode('utf-8')
        # cookie = re.sub(r'\s?path=/;?', '', cookie)
        # cookie = 'Ecp_ClientId=4181203190702387619; UM_distinctid=16773c08bf2617-073c38f3ffa235-3d740c5e-1fa400-16773c08bf3121f; Ecp_IpLoginFail=181215111.202.192.3; ASP.NET_SessionId=lrjw4gaufyffpzlfvfdzmbq0; SID_kns=123114; SID_klogin=125142; ASPSESSIONIDQSSBATBC=PGHJBPLBHDJLMOPDFGIJLHHD; KNS_SortType=; RsPerPage=20; SID_krsnew=125133; cnkiUserKey=92eb3dfa-62de-0145-a6a0-9d5ed32636ab; SID_kxreader_new=011121; SID_kcms=124102; _pk_ref=%5B%22%22%2C%22%22%2C1544874781%2C%22http%3A%2F%2Fwww.cnki.net%2F%22%5D; _pk_ses=*'
        # cookie = 'Ecp_ClientId=6181215120000182507; Ecp_IpLoginFail=181215111.202.192.3; SID=011104; ASP.NET_SessionId=1f4a5d3uv0illr1x3i2prkzv; SID_kns=011106; KNS_SortType='
        # cookie = 'Ecp_ClientId=4181203190702387619; UM_distinctid=16773c08bf2617-073c38f3ffa235-3d740c5e-1fa400-16773c08bf3121f; Ecp_IpLoginFail=181215111.202.192.3; ASP.NET_SessionId=lrjw4gaufyffpzlfvfdzmbq0; SID_kns=123114; SID_klogin=125142; ASPSESSIONIDQSSBATBC=PGHJBPLBHDJLMOPDFGIJLHHD; KNS_SortType=; RsPerPage=20; SID_krsnew=125133; cnkiUserKey=92eb3dfa-62de-0145-a6a0-9d5ed32636ab; SID_kxreader_new=011121; SID_kcms=124102; _pk_ref=%5B%22%22%2C%22%22%2C1544874781%2C%22http%3A%2F%2Fwww.cnki.net%2F%22%5D; _pk_ses=*'

        url = 'http://nvsm.cnki.net/kns/brief/brief.aspx?pagename={resp_str}&t={timestamp}&keyValue=&S=1&sorttype=' \
            .format(resp_str=response.text, timestamp=1000 * time.time())
        yield Request(url=url, callback=self.parse_search_result, headers=response.meta['headers'], meta=response.meta)

    def parse_search_result(self, response):
        # print(response.text)
        base_url = 'http://nvsm.cnki.net'

        # paper_urls = response.xpath('//*[@class="fz14"]/@href').extract()  # 当前页中的所有结果
        # print("当前页面中结果数量： ", len(paper_urls))
        # for url_tail in paper_urls:  # 解析每一页中的结果
        #     url = base_url + url_tail
        #     yield Request(url=url, callback=self.parse_user_info, headers=response.meta['headers'], meta=response.meta)
        try:
            authors_link = response.xpath('//*[@class="KnowledgeNetLink"]/@href').extract()
        except Exception as e:
            print("无法获取作者信息。", e)
            authors_link = []

        print("authors_link: ", len(authors_link))

        for link in authors_link:
            info = parse.unquote(link)
            tail = author_code_pat.findall(info)
            if len(tail) > 0:
                self.author['url'] = 'http://nvsm.cnki.net/kns/popup/knetsearchNew.aspx?' + tail[0]
                yield self.author

        try:
            pages_info = response.xpath('//*[@class="TitleLeftCell"]/a/text()').extract()
        except Exception as e:
            print("无法获取页数信息。", e)
            pages_info = []

        if len(pages_info) > 1:
            total_pages = int(pages_info[-2])
            print("total_pages: ", total_pages)

            for page in range(2, total_pages + 1):
                turn_page_url = "http://nvsm.cnki.net/kns/brief/brief.aspx?curpage={curpage}&RecordsPerPage=20&" \
                                "QueryID={queryId}&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&" \
                                "DisplayMode=listmode&PageName=ASP.brief_result_aspx&isinEn=1&" \
                    .format(curpage=page, queryId=response.meta['queryID'])

                url = 'http://nvsm.cnki.net/kns/brief/brief.aspx?' + turn_page_url
                yield Request(url=url, callback=self.parse_search_result,
                              headers=response.meta['headers'], meta=response.meta)
