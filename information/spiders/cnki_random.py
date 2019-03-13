# -*- coding: utf-8 -*-
import os
import re
import time
import scrapy
import requests
from lxml import etree
from scrapy.http import Request
from information.items import Paper


class CnkiRandomSpider(scrapy.Spider):
    name = 'cnki_random'
    allowed_domains = ['cnki.net']

    def start_requests(self):
        # 1、使用姓名和单位检索（POST）; 2、使用返回的cookie去get结果即可。
        url = 'http://kns.cnki.net/kns/request/SearchHandler.ashx'

        pwd = os.path.dirname(__file__)
        in_file = os.path.join(pwd, "../../resources/cnki.buzhua.keywords.txt")

        with open(in_file) as f:
            for idx, line in enumerate(f):
                word = line.strip()
                print(idx, " ", word)
                # 关键字 检索
                keyword_formdata = {
                    'action': '',
                    'ua': '1.11',
                    'isinEn': '1',
                    'PageName': 'ASP.brief_default_result_aspx',
                    'DbPrefix': 'SCDB',
                    'DbCatalog': '中国学术文献网络出版总库',
                    'ConfigFile': 'SCDBINDEX.xml',
                    'db_opt': 'CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
                    'txt_1_sel': 'KY$=|',
                    'txt_1_value1': word,
                    'txt_1_special1': '%',
                    'his': '0',
                    'parentdb': 'SCDB',
                    '__': '{} GMT+0800 (中国标准时间)'.format(time.strftime("%a %b %d %Y %H:%M:%S", time.localtime())),
                }
                # cookie 信息有可能需要从自己的 chrome -> 检查 -> network 中搜索一次拿到
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
                    formdata=keyword_formdata,
                    callback=self.get_search_result_page,
                    headers=headers,
                    meta={'headers': headers, 'queryID': idx+1}
                )

                # 主题 检索
                topic_formdata = {
                    'action': '',
                    'ua': '1.11',
                    'isinEn': '1',
                    'PageName': 'ASP.brief_default_result_aspx',
                    'DbPrefix': 'SCDB',
                    'DbCatalog': '中国学术文献网络出版总库',
                    'ConfigFile': 'SCDBINDEX.xml',
                    'db_opt': 'CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
                    'txt_1_sel': 'SU$%=|',
                    'txt_1_value1': word,
                    'txt_1_special1': '%',
                    'his': '0',
                    'parentdb': 'SCDB',
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
                    formdata=topic_formdata,
                    callback=self.get_search_result_page,
                    headers=headers,
                    meta={'headers': headers, 'queryID': idx + 1}
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

        url = 'http://kns.cnki.net/kns/brief/brief.aspx?pagename={resp_str}&t={timestamp}&keyValue=&S=1&sorttype='\
            .format(resp_str=response.text, timestamp=1000 * time.time())
        yield Request(url=url, callback=self.parse_search_result, headers=response.meta['headers'], meta=response.meta)

    def parse_search_result(self, response):
        # print(response.text)
        base_url = 'http://kns.cnki.net'

        paper_urls = response.xpath('//*[@class="fz14"]/@href').extract()  # 当前页中的所有结果
        # print("当前页面中结果数量： ", len(paper_urls))
        for url_tail in paper_urls:  # 解析每一页中的结果
            url = base_url + url_tail
            yield Request(url=url, callback=self.parse_paper_info, headers=response.meta['headers'], meta=response.meta)

        try:
            pages_info = response.xpath('//*[@class="TitleLeftCell"]/a/text()').extract()
        except Exception as e:
            print("无法获取页数信息。", e)
            pages_info = []

        if len(pages_info) > 1:
            total_pages = int(pages_info[-2])

            for page in range(2, total_pages+1):
                turn_page_url = "http://kns.cnki.net/kns/brief/brief.aspx?curpage={curpage}&RecordsPerPage=20&" \
                                "QueryID={queryId}&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&" \
                                "DisplayMode=listmode&PageName=ASP.brief_result_aspx&isinEn=1"\
                    .format(curpage=page, queryId=response.meta['queryID'])

                url = 'http://kns.cnki.net/kns/brief/brief.aspx?' + turn_page_url
                yield Request(url=url, callback=self.parse_search_result,
                              headers=response.meta['headers'], meta=response.meta)

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
