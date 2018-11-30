# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.conf import settings
import pymongo

class CodeforcesCrawlerPipeline(object):

    def __init__(self):
        self.items_nums = 0

        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        self.client.admin.authenticate(settings['MONGO_USER'], settings['MONGO_PASSWORD'])
        self.db = self.client[settings['MONGO_DB']]
        self.collection = self.db[settings['MONGO_COLLECTION']]

    def process_item(self, item, spider):
        self.items_nums += 1
        self.collection.insert(dict(item))
        if self.items_nums % 100 ==0:
            	print("%d items have been collected." % self.items_nums)
        return item

    # spider_closed() function is deprecated.
    def close_spider(self, spider):
        self.client.close()
