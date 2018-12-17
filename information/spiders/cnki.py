# -*- coding: utf-8 -*-
import re
import time
import scrapy
import urllib.parse
from scrapy.http import Request


class CnkiSpider(scrapy.Spider):
    name = 'cnki'
    allowed_domains = ['cnki.net']
    # start_urls = [
    #     'http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB&crossDbcodes=CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
    # ]

    def start_requests(self):
        # 1、使用姓名和单位检索（POST）; 2、使用返回的cookie去get结果即可。
        url = 'http://kns.cnki.net/kns/request/SearchHandler.ashx'
        # author = '周昌令'
        # school = '北京大学'
        # time_str = 'Sat Dec 15 2018 12:15:06 GMT+0800 (中国标准时间)'
        # str_data = 'action=&NaviCode=*&ua=1.21&isinEn=1&PageName=ASP.brief_result_aspx&' \
        #            'DbPrefix=SCDB&DbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&' \
        #            'ConfigFile=SCDB.xml&db_opt=CJFQ%2CCDFD%2CCMFD%2CCPFD%2CIPFD%2CCCND%2CCCJD&au_1_sel=AU&au_1_sel2=AF&' \
        #            'au_1_value1={author}' \
        #            'au_1_value2={school}' \
        #            'au_1_special1=%3D&au_1_special2=%25&his=0&' \
        #            '__={time_info}'.format(author=urllib.parse.quote(author), school=urllib.parse.quote(school),
        #                                    time_info=urllib.parse.quote(time_str))
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
            'au_1_special1': '=',
            'au_1_special2': '%',
            'his': '0',
            '__': '{} GMT+0800 (中国标准时间)'.format(time.strftime("%a %b %d %Y %H:%M:%S",time.localtime())),
        }
        # new_data = 'action=&NaviCode=*&ua=1.21&isinEn=1&PageName=ASP.brief_result_aspx&DbPrefix=SCDB&DbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDB.xml&db_opt=CJFQ%2CCDFD%2CCMFD%2CCPFD%2CIPFD%2CCCND%2CCCJD&au_1_sel=AU&au_1_sel2=AF&au_1_value1=%E5%B0%9A%E7%BE%A4&au_1_value2=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6&au_1_special1=%3D&au_1_special2=%25&his=0&__=Sat%20Dec%2015%202018%2012%3A25%3A50%20GMT%2B0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)'
        # print(str_data)
        # print(new_data)
        # print(urllib.parse.urlencode(formdata))

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
            meta={'headers': headers}
        )

    def parse(self, response):
        # print('headers: ', response.headers)
        # cookie_list = response.headers.getlist('Set-Cookie')
        # cookie = b''.join(cookie_list).decode('utf-8')
        # cookie = re.sub(r'\s?path=/;?', '', cookie)
        cookie = 'Ecp_ClientId=4181203190702387619; UM_distinctid=16773c08bf2617-073c38f3ffa235-3d740c5e-1fa400-16773c08bf3121f; Ecp_IpLoginFail=181215111.202.192.3; ASP.NET_SessionId=lrjw4gaufyffpzlfvfdzmbq0; SID_kns=123114; SID_klogin=125142; ASPSESSIONIDQSSBATBC=PGHJBPLBHDJLMOPDFGIJLHHD; KNS_SortType=; RsPerPage=20; SID_krsnew=125133; cnkiUserKey=92eb3dfa-62de-0145-a6a0-9d5ed32636ab; SID_kxreader_new=011121; SID_kcms=124102; _pk_ref=%5B%22%22%2C%22%22%2C1544874781%2C%22http%3A%2F%2Fwww.cnki.net%2F%22%5D; _pk_ses=*'
        # cookie = 'Ecp_ClientId=6181215120000182507; Ecp_IpLoginFail=181215111.202.192.3; SID=011104; ASP.NET_SessionId=1f4a5d3uv0illr1x3i2prkzv; SID_kns=011106; KNS_SortType='
        # cookie = 'Ecp_ClientId=4181203190702387619; UM_distinctid=16773c08bf2617-073c38f3ffa235-3d740c5e-1fa400-16773c08bf3121f; Ecp_IpLoginFail=181215111.202.192.3; ASP.NET_SessionId=lrjw4gaufyffpzlfvfdzmbq0; SID_kns=123114; SID_klogin=125142; ASPSESSIONIDQSSBATBC=PGHJBPLBHDJLMOPDFGIJLHHD; KNS_SortType=; RsPerPage=20; SID_krsnew=125133; cnkiUserKey=92eb3dfa-62de-0145-a6a0-9d5ed32636ab; SID_kxreader_new=011121; SID_kcms=124102; _pk_ref=%5B%22%22%2C%22%22%2C1544874781%2C%22http%3A%2F%2Fwww.cnki.net%2F%22%5D; _pk_ses=*'
        # print('cookie: ', cookie)
        # print("url: ", response.url)
        # print("text: ", response.text)
        # # print("headers: ", response.headers)
        # # print(response)
        # print('-' * 80)

        url = 'http://kns.cnki.net/kns/brief/brief.aspx?pagename={resp_str}&t={timestamp}&keyValue=&S=1&sorttype='\
            .format(resp_str=response.text, timestamp=1000 * time.time())
        yield Request(url=url, callback=self.parse_page, headers=response.meta['headers'], meta=response.meta)

    def parse_page(self, response):
        # print('new request cookies: ', response.headers.getlist('Cookies'))
        # print('new response cookies: ', response.headers.getlist('Set-Cookies'))
        # print('url: ', response.url)
        # print('headers: ', response.headers)
        # print('body: ', response.body)
        # print('text: ', response.text)
        base_url = 'http://kns.cnki.net/'

        paper_url = response.xpath('//*[@class="fz14"]/@href').extract()
        # print(paper_url)
        url = base_url + paper_url[0]
        yield Request(url=url, callback=self.parse_info, headers=response.meta['headers'], meta=response.meta)

    def parse_info(self, response):
        print(response.text)
        # pass