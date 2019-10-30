# import scrapy
# import json
# from myspider.items import MyspiderItem
#
# class DoubanMovieSpider(scrapy.Spider):
#     name = 'douban_movie'
#     allowed_domains = ['movie.douban.com']
#     start_urls = ['https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=0&limit=20']
#     offset = 0
#     def parse(self, response):
#         item = DoubanItem()
#         content_list = json.loads(response.body.decode())
#         if (content_list == []):
#             return
#         for content in content_list:
#             item['title'] = content['title']
#             item['url'] = content['url']
#             yield item
#         self.offset += 20
#         url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start='+str(self.offset) + '&limit=20'
#         yield scrapy.Request(url=url,callback=self.parse)

# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
from scrapy import Request
from myspider.items import MyspiderItem
import re
import json

class doubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ["douban.com"]
    start_list = []
    for i in range(1,14):
        url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=' + str(i*20)
        start_list.append(url)
    start_urls = start_list

    def start_requests(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, method='GET', callback=self.parse)

    def parse(self, response):
        hxs = response.body.decode('utf-8')
        hjson = json.loads(hxs)
        for lis in hjson['subjects']:
            item = MyspiderItem()
            item["info"] = lis['url']
            item["pic"] = lis['cover']
            item["score"] = lis['rate']
            item["title"] = lis['title']
            filename = item["title"] + '_' + item["score"] + 'min' + '.jpg'
            # requests.urlretrieve(item["pic"], filename)
            yield item