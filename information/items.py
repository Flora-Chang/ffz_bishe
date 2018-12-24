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
    title = scrapy.Field()
    authors = scrapy.Field()
    authors_orgs = scrapy.Field()
    abstract = scrapy.Field()
    keywords = scrapy.Field()
    class_num = scrapy.Field()
    references = scrapy.Field()
    similar_liters = scrapy.Field()
    reader_recs = scrapy.Field()