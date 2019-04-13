# -*- coding: utf-8 -*-
import re
import time
import json
import scrapy
from scrapy.http import Request

from information.items import AuthorInfo


class CnkiAuthorInfoSpider(scrapy.Spider):
    name = 'cnki_author_info'
    allowed_domains = ['cnki.net']

    def __init__(self, url=None, *args, **kwargs):
        super(CnkiAuthorInfoSpider, self).__init__(*args, **kwargs)
        self.author_info = AuthorInfo()
        self.base_url = 'http://kns.cnki.net/kcms/detail/'
        self.url = json.loads(url)['url']
        self.link_pat = re.compile(r"'(frame/knetlist.aspx.*=\w+)'")
        self.page_bar_pat = re.compile(r'ShowPage\((.*)\);')
        self.collaborator_pat = re.compile(r"TurnPageToKnet\('au','(.*?)','(\d+)'\)")

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
        self.author_info['name'] = name

        org = response.xpath('//*[@class="info"]/p/a/text()').extract()
        self.author_info['org'] = org

        domain = response.xpath('//*[@class="info"]/p[2]/text()').extract()
        self.author_info['domain'] = domain

        num = response.xpath('//*[@class="info"]/p[3]/span/text()').extract()
        num = [x.strip() for x in num]
        if len(num) == 2:
            pub_num = re.findall(r'(\d+)', num[0])
            if len(pub_num) == 1:
                self.author_info['pub_num'] = int(pub_num[0])

            download_num = re.findall(r'(\d+)', num[1])
            if len(download_num) == 1:
                self.author_info['download_num'] = int(download_num[0])

        cont_right = response.xpath('//*[@class="contRight"]').extract()
        cont_right = self.link_pat.findall(cont_right[0])
        cont_right.append('end')
        print(cont_right)

        for idx, link in enumerate(cont_right):
            link = self.base_url + link
            if link.endswith('&infotype=1'):  # 关注领域 OK
                callback_fun = self.parse_targets
            elif link.endswith('&infotype=3'):  # 作者文献（最高被引， 最高下载） OK
                callback_fun = self.parse_zuozhe_wenxian
            elif link.endswith('&infotype=4&codetype=1'):  # 发表在期刊上的文献 OK
                callback_fun = self.parse_qikan
            elif link.endswith('&infotype=15&codetype=au'):  # 外文期刊 OK
                callback_fun = self.parse_waiwen_qikan
            elif link.endswith('&infotype=4&codetype=4'):  # 发表在报纸上的文献
                continue
                callback_fun = self.parse_waiwen_qikan
            elif link.endswith('&infotype=4&codetype=3'):  # 发表在会议上的文献  OK
                callback_fun = self.parse_huiyi
            elif link.endswith('&infotype=4&codetype=2'):  # 发表在博硕上的文献
                continue
                callback_fun = self.parse_waiwen_qikan
            elif link.endswith('&infotype=5'):  # 曾参考的文献 OK
                callback_fun = self.parse_ceng_cankao
            elif link.endswith('&infotype=6'):  # 作者的导师
                continue
                callback_fun = self.parse_daoshi
            elif link.endswith('&infotype=7'):  # 合作作者 OK
                callback_fun = self.parse_collaborators
            elif link.endswith('&infotype=2'):  # 获得支持基金 OK
                callback_fun = self.parse_zhichi_jijin
            elif link.endswith('&infotype=8'):  # 指导的学生
                continue
                callback_fun = self.parse_zhidao_xuesheng
            else:
                callback_fun = self.parse_end
                link = 'http://kns.cnki.net'

            # 最后一个执行的必须 yield self.author_info 以写出结果
            yield Request(url=link, callback=callback_fun, priority=len(cont_right)-idx)

    def parse_targets(self, response):  # 关注领域, OK
        targets = response.xpath('//*[@target="kcmstarget"]/text()').extract()
        self.author_info['targets'] = targets

    def parse_zuozhe_wenxian(self, response):   # 发文总量, 下载总量, 最高被引, 最高下载 OK
        title_side = response.xpath('//*[@class="titleSide"]/span/b/text()').extract()  # [发文总量, 下载总量]
        if len(title_side) == 2:
            if 'pub_num' not in self.author_info:
                self.author_info['pub_num'] = int(title_side[0])
            if 'download_num' not in self.author_info:
                self.author_info['download_num'] = int(title_side[1])

        zuigao_beiyin_url = response.xpath('//*[@class="essayBox"]//*[@target="kcmstarget"]/@href').extract()
        zuigao_beiyin_url = [self.base_url + url for url in zuigao_beiyin_url]
        zuigao_beiyin_name = response.xpath('//*[@class="essayBox"]//*[@target="kcmstarget"]/text()').extract()
        zuigao_beiyin_num = response.xpath('//*[@class="essayBox"]//*[@target="kcmstarget"]/../b/text()').extract()
        self.author_info['zuigao_beiyin'] = list(zip(zuigao_beiyin_url, zuigao_beiyin_name, zuigao_beiyin_num))
        # print("最高被引：", self.author_info['zuigao_beiyin'])

        zuigao_xiazai_url = response.xpath('//*[@class="essayBox border"]//*[@target="kcmstarget"]/@href').extract()
        zuigao_xiazai_url = [self.base_url + url for url in zuigao_xiazai_url]
        zuigao_xiazai_name = response.xpath('//*[@class="essayBox border"]//*[@target="kcmstarget"]/text()').extract()
        zuigao_xiazai_num = response.xpath('//*[@class="essayBox border"]//*[@target="kcmstarget"]/../b/text()').extract()
        self.author_info['zuigao_xiazai'] = list(zip(zuigao_xiazai_url, zuigao_xiazai_name, zuigao_xiazai_num))
        # print("最高下载：", self.author_info['zuigao_xiazai'])

    def parse_qikan(self, response):  # 发表在期刊上的论文, OK
        qikan_url = response.xpath('//*[@target="kcmstarget"]/@href').extract()
        qikan_url = [self.base_url + url for url in qikan_url]

        qikan_name = response.xpath('//*[@target="kcmstarget"]/text()').extract()
        tmp_qikan = list(zip(qikan_url, qikan_name))

        total_num = response.xpath('//*[@id="pc_CJFQ"]/text()').extract()
        if len(total_num) == 1:
            total_num = int(total_num[0])
        else:
            total_num = len(tmp_qikan)
        self.author_info['qikan_num'] = total_num
        self.author_info['qikan'] = tmp_qikan
        # print("total_num: ", self.author_info['qikan_num'])

        self.author_info['qikan'] = tmp_qikan
        # print("发表在期刊上的论文: ", len(self.author_info['qikan']), self.author_info['qikan'])

    def parse_waiwen_qikan(self, response):
        qikan_url = response.xpath('//*[@target="kcmstarget"]/@href').extract()
        qikan_url = [self.base_url + url for url in qikan_url]

        qikan_name = response.xpath('//*[@target="kcmstarget"]/text()').extract()
        tmp_qikan = list(zip(qikan_url, qikan_name))

        total_num = response.xpath('//*[@id="pc_WWJD"]/text()').extract()
        if len(total_num) == 1:
            total_num = int(total_num[0])
        else:
            total_num = len(tmp_qikan)
        self.author_info['waiwen_qikan_num'] = total_num
        self.author_info['waiwen_qikan'] = tmp_qikan
        # print("waiwen_total_num: ", self.author_info['waiwen_qikan_num'])

    def parse_huiyi(self, response):    # 发表在会议上的文章 OK
        qikan_url = response.xpath('//*[@target="kcmstarget"]/@href').extract()
        qikan_url = [self.base_url + url for url in qikan_url]

        qikan_name = response.xpath('//*[@target="kcmstarget"]/text()').extract()
        tmp_qikan = list(zip(qikan_url, qikan_name))

        total_num = response.xpath('//*[@id="pc_CPFD"]/text()').extract()
        if len(total_num) == 1:
            total_num = int(total_num[0])
        else:
            total_num = len(tmp_qikan)
        self.author_info['huiyi_num'] = total_num
        self.author_info['huiyi'] = tmp_qikan
        # print("total_num: ", self.author_info['huiyi_num'])

    def parse_zhichi_jijin(self, response):     # 获得支持基金 OK
        zhichi_jijin = response.xpath('//*[@target="kcmstarget"]/text()').extract()
        jijin_num = response.xpath('//*[@target="kcmstarget"]/../b/text()').extract()
        jijin_num = [int(num.strip().lstrip('(').rstrip(')')) for num in jijin_num]
        self.author_info['zhichi_jijin'] = list(zip(zhichi_jijin, jijin_num))
        # print("获得支持基金:", self.author_info['zhichi_jijin'])
        # yield self.author_info

    def parse_ceng_cankao(self, response):  # 曾参考的文献 OK
        ceng_cankao_url = response.xpath('//*[@target="kcmstarget"]/@href').extract()
        ceng_cankao_url = [self.base_url + url for url in ceng_cankao_url]
        ceng_cankao_name = response.xpath('//*[@target="kcmstarget"]/text()').extract()
        tmp_cankao = list(zip(ceng_cankao_url, ceng_cankao_name))
        total_num = response.xpath('//*[@id="pc_CPFD"]/text()').extract()
        if len(total_num) == 1:
            total_num = int(total_num[0])
        else:
            total_num = len(tmp_cankao)
        self.author_info['ceng_cankao_num'] = total_num
        self.author_info['ceng_cankao'] = tmp_cankao
        # print("曾参考的文献:", self.author_info['ceng_cankao'])

    def parse_collaborators(self, response):
        same_collaborators = []
        same_org = response.xpath('//*[@class="coopAuthor"]/div[1]//*[@target="kcmstarget"]/@onclick').extract()
        for info in same_org:
            same_collaborators.extend(self.collaborator_pat.findall(info))
        same_collaborators = [(x[0], int(x[1])) for x in same_collaborators]
        self.author_info['same_org_collaborator'] = same_collaborators

        other_collaborators = []
        other_org = response.xpath('//*[@class="coopAuthor"]/div[2]//*[@target="kcmstarget"]/@onclick').extract()
        for info in other_org:
            other_collaborators.extend(self.collaborator_pat.findall(info))
        other_collaborators = [(x[0], int(x[1])) for x in other_collaborators]
        self.author_info['other_org_collaborator'] = other_collaborators

    def parse_zhidao_xuesheng(self):
        # yield self.author_info
        pass

    def parse_end(self, reponse):
        yield self.author_info
