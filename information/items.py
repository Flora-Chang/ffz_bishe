# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InformationItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    publish_time = scrapy.Field()
    article = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    author_danwei = scrapy.Field()
    keyword = scrapy.Field()


class Paper(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    author_orgs = scrapy.Field()
    abstract = scrapy.Field()
    keywords = scrapy.Field()
    # fund = scrapy.Field()         # 基金
    class_nums = scrapy.Field()         # 分类号
    references = scrapy.Field()         # 引用文献
    similar_liters = scrapy.Field()     # 相似文献
    reader_recs = scrapy.Field()        # 读者推荐


class Author(scrapy.Item):
    url = scrapy.Field()


class AuthorInfo(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    org = scrapy.Field()  # 单位
    domain = scrapy.Field()  # 研究方向
    pub_num = scrapy.Field()  # 总发文量
    download_num = scrapy.Field()  # 总下载量
    targets = scrapy.Field()  # 关注领域
    zuigao_beiyin = scrapy.Field()  # 最高被引
    zuigao_xiazai = scrapy.Field()  # 最高下载
    qikan = scrapy.Field()  # 发表在期刊上的论文
    qikan_num = scrapy.Field()  # 发表在期刊上的论文数量

    waiwen_qikan = scrapy.Field()   # 外文期刊文章
    waiwen_qikan_num = scrapy.Field()   # 外文期刊文章数量

    huiyi = scrapy.Field()  # 发表在会议上的论文
    huiyi_num = scrapy.Field()  # 发表在会议上的论文数量

    ceng_cankao = scrapy.Field()    # 层参考的文献
    ceng_cankao_num = scrapy.Field()  # 层参考的文献数量
    zhichi_jijin = scrapy.Field()   # 获得支持基金

    same_org_collaborator = scrapy.Field()  # 同机构主要合作者
    other_org_collaborator = scrapy.Field()  # 其他机构主要合作者

    daoshi = scrapy.Field()     # 导师
    xuesheng = scrapy.Field()   # 指导的学生


