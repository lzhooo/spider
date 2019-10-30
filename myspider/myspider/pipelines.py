# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# class MyspiderPipeline(object):
#     def process_item(self, item, spider):
#         return item



from scrapy import Item
import pymongo
import json
import sys
import settings
reload(sys)
sys.setdefaultencoding( "utf-8" )

class MyspiderPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        cls.DB_URL = crawler.settings.get('MONGO_DB_URI', 'mongodb://localhost:27017')
        cls.DB_NAME = crawler.settings.get('MONGO_DB_NAME', 'douban')
        return cls()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URL)
        self.db = self.client[self.DB_NAME]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'douban':
            collection = self.db[spider.name]
            post = dict(item) if isinstance(item, Item) else item
            post['score'] = ''
            m = collection.find({"title": post['title'],"score":post['score']}).count()
            if(m):
                pass
            else:
                n = collection.find({"title": post['title']}).count()
                if(n):
                    collection.update({"title": post['title']}, {"$set": {"score": post['score']}})
                else:
                    collection.insert_one(post)
        if spider.name == 'bilibili':
            collection = self.db[spider.name]
            post = dict(item) if isinstance(item, Item) else item
            # post['play'] = ''
            m = collection.find({"title": post['title'],"play":post['play']}).count()
            if(m):
                pass
            else:
                n = collection.find({"title": post['title']}).count()
                if(n):
                    collection.update({"title": post['title']}, {"$set": {"play": post['play'],"comment":post['comment']}})
                else:
                    collection.insert_one(post)
        if spider.name == 'bilibilitm' or spider.name == 'bilibilitm_yzye':
            db = self.client[spider.name]
            post = dict(item) if isinstance(item, Item) else item
            if len(post['title']) > 100:
                post['title'] = post[title][0:100] + "..."
            collection = db[post['title']]
            del post['title']
            del post['url']
            del post['spider']
            del post['domain']
            del post['timestamp']
            collection.insert_one(post)
        return item
