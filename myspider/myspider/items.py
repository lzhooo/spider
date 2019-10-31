# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # title = scrapy.Field()
    # url = scrapy.Field()
    timestamp = scrapy.Field()
    url = scrapy.Field()
    info = scrapy.Field()
    pic = scrapy.Field()
    score = scrapy.Field()
    title = scrapy.Field()
    domain = scrapy.Field()
    spider = scrapy.Field()

class BilibiliItem(scrapy.Item):
    timestamp = scrapy.Field()
    url = scrapy.Field()
    domain = scrapy.Field()
    spider = scrapy.Field()
    title = scrapy.Field()
    pic = scrapy.Field()
    length = scrapy.Field()
    favorites = scrapy.Field()
    aid = scrapy.Field()
    play = scrapy.Field()
    comment = scrapy.Field()

class BilibiliTMItem(scrapy.Item):
    timestamp = scrapy.Field()
    url = scrapy.Field()
    domain = scrapy.Field()
    spider = scrapy.Field()
    aid = scrapy.Field()
    cid = scrapy.Field()
    tanmu = scrapy.Field()