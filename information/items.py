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
    doma = scrapy.Field()  # 眼睛方向
    pub_num = scrapy.Field()  # 总发文量
    download_num = scrapy.Field()  # 总下载量
