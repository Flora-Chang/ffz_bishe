# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
import codecs

class InformationPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'pkuResearch':
            filename = 'pkuresearch.json'
        elif spider.name == 'cutech':
            filename = 'cutech.json'
        elif spider.name == 'cistc':
            filename = 'cistc.json'
        elif spider.name == 'nsfc':
            filename = 'nsfc.json'
        elif spider.name == 'moe':
            filename = 'moe.json'
        elif spider.name == 'npd_nsfc':
            filename = 'npd_nsfc.json'
        elif spider.name == 'cnki':
            filename = 'cnki.json'
        elif spider.name == 'cnki_buzhua':
            filename = 'cnki.buzhua.201904.json'
        elif spider.name == 'cnki_random':
            filename = 'cnki.random.json'
        elif spider.name == 'cnki_authors':
            filename = 'cnki.authors.json'
        elif spider.name == 'cnki_author_info':
            filename = 'cnki.author_info.d.json'
        else:
            filename = 'others.json'

        filename = os.path.join("data/", filename)

        with codecs.open(filename, mode='a', encoding='utf-8') as fout:
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            fout.write(line)
        return item

