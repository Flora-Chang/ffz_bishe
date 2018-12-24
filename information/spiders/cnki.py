# -*- coding: utf-8 -*-
import re
import time
import scrapy
import urllib.parse
from scrapy.http import Request
from information.items import Paper


class CnkiSpider(scrapy.Spider):
    name = 'cnki'
    allowed_domains = ['cnki.net']
    # start_urls = [
    #     'http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB&crossDbcodes=CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
    # ]

    def start_requests(self):
        # 1、使用姓名和单位检索（POST）; 2、使用返回的cookie去get结果即可。
        url = 'http://kns.cnki.net/kns/request/SearchHandler.ashx'

        researchers_info = [('陈萍', '北京大学'), ('马浩', '北京大学'), ('周昌令', '北京大学')]

        for idx, researcher in enumerate(researchers_info[0]):
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
                'au_1_value1': '陈萍',  # researcher[0],
                'au_1_value2': '北京大学',  # researcher[1],
                'au_1_special1': '=',
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
                callback=self.get_search_result_page,
                headers=headers,
                meta={'headers': headers, 'queryID': idx+1}
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
        base_url = 'http://kns.cnki.net/'

        paper_urls = response.xpath('//*[@class="fz14"]/@href').extract()  # 当前页中的所有结果
        print("当前页面中结果数量： ", len(paper_urls))
        for url_tail in paper_urls:  # 解析每一页中的结果
            url = base_url + url_tail
            yield Request(url=url, callback=self.parse_paper_info, headers=response.meta['headers'], meta=response.meta)
            break

        # if 'tailPages' in response.meta:
        #     print(response.text)
        #
        # if 'tailPages' not in response.meta:
        #     pages_info = response.xpath('//*[@class="TitleLeftCell"]/a/text()').extract()
        #     print("pages_info: ", len(pages_info))
        #     if len(pages_info) > 1:
        #         total_pages = int(pages_info[-2])
        #         print("总页数： ", total_pages)
        #
        #         for page in range(2, total_pages+1):  # 翻页，先确定总数
        #             print("---第{}页---".format(page))
        #             turn_page_url = "http://kns.cnki.net/kns/brief/brief.aspx?curpage={curpage}&RecordsPerPage=20&" \
        #                             "QueryID={queryId}&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&" \
        #                             "DisplayMode=listmode&PageName=ASP.brief_result_aspx&isinEn=1"\
        #                 .format(curpage=page, queryId=response.meta['queryID'])
        #
        #             response.meta['tailPages'] = False
        #             url = 'http://kns.cnki.net/kns/brief/brief.aspx?' + turn_page_url
        #             yield Request(url=url, callback=self.parse_search_result,
        #                           headers=response.meta['headers'], meta=response.meta)
        #             break

    def parse_paper_info(self, response):
        # print(response.text)

        title = response.xpath('//*[@class="title"]/text()').extract()[0]
        authors = response.xpath('//*[@class="author"]/span/a/text()').extract()
        author_danweis = response.xpath('//*[@class="orgn"]/span/a/text()').extract()
        author_danwei = ' '.join(author_danweis)
        article = response.xpath('//*[@id="ChDivSummary"]/text()').extract()[0]
        keywords = response.xpath('//*[@class="wxBaseinfo"]/p[3]/a/text()').extract()
        keyword = [re.sub(r'[;\r\n +]+', '', k) for k in keywords]
        tags = response.xpath('//*[@class="wxBaseinfo"]/p[4]/text()').extract()

        note = response.xpath('//*[@class="btn-note"]/@href').extract()[0]
        db_info = re.findall(r'testlunbo\?(.*)&filesourcetype=1', note)[0]

        # reference_url = 'http://kns.cnki.net/kcms/detail/frame/list.aspx?{}&RefType=1&vl='.format(db_info)
        # yield Request(url=reference_url, callback=self.parse_references)

        # similar_liter_url = 'http://kns.cnki.net/kcms/detail/frame/asynlist.aspx?{}&reftype=604' \
        #                     '&catalogId=lcatalog_func604&catalogName=%E7%9B%B8%E4%BC%BC%E6%96%87%E7%8C%AE%0A%20%20%20' \
        #                     '%20%20%20%20%20%20%20'.format(db_info)
        # yield Request(url=similar_liter_url, callback=self.parse_similar_literature)

        # reader_rec_url = 'http://kns.cnki.net/kcms/detail/frame/asynlist.aspx?{}&reftype=605&catalogId=lcatalog_func605' \
        #                  '&catalogName=%E8%AF%BB%E8%80%85%E6%8E%A8%E8%8D%90%0A%20%20%20%20%20%20%20%20%20%20'.format(db_info)
        # yield Request(url=reader_rec_url, callback=self.parse_reader_recommendation)

        paper = Paper()
        paper['title'] = title
        # # post['publish_time'] = publish_time
        # paper['author'] = authors
        # paper['article'] = article
        # paper['keyword'] = keyword
        # paper['tags'] = tags
        # paper['author_danwei'] = author_danwei
        # paper['url'] = response.url

        # yield paper

        # print(response.text)
        # pass
        # 请求引用，相似文献等

    def parse_references(self, response):
        # 参考文献格式不一致，还有翻页
        refers = response.xpath('//*[@target="kcmstarget"]').extract()
        # print(response.text)
        print(len(refers))
        # print("refers: ", refers)
        for refer in refers:
            print(refer)

    def parse_similar_literature(self, response):  # ok
        similar_liters = []
        base_url = 'http://kns.cnki.net/'
        # print(response.text)
        refers = response.xpath('//*[@target="kcmstarget"]').extract()
        # print("refers: ", refers)
        for refer in refers:
            url = base_url + re.findall(r'href="(.*)">', refer)[0]
            title = re.findall(r'">(.*)</a>', refer)[0]
            similar_liters.append((title, url))
        return similar_liters

    def parse_reader_recommendation(self, response):
        print(response.text)

    def parse_associated_author(self, response):
        pass