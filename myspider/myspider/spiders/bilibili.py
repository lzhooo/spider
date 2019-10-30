
import scrapy
from scrapy.selector import Selector
from scrapy import Request
from myspider.items import BilibiliItem,BilibiliTMItem
import re
import json

class bilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    allowed_domains = ["bilibili.com"]
    start_list = []
    for i in range(1,4):
        url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=250858633&pagesize=100&tid=0&page=' + str(i) + '&keyword=&order=pubdate'
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
        hjson2 = hjson['data']

        for lis in hjson2['vlist']:
            item = BilibiliItem()
            item["title"] = lis['title']
            item["pic"] = lis['pic']
            item["length"] = lis['length']
            item["favorites"] = lis['favorites']
            item["aid"] = lis['aid']
            item["play"] = lis['play']
            item["comment"] = lis['comment']
            yield item


class bilibiliTMSpider(scrapy.Spider):
    name = 'bilibilitm_yzye'
    allowed_domains = ["bilibili.com"]
    start_list = []
    for i in range(1,15):
        url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=95515699&pagesize=100&tid=0&page=' + str(i) + '&keyword=&order=pubdate'
        start_list.append(url)
    start_urls = start_list

    def start_requests(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, method='GET', callback=self.parse)

    def parse(self, response):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        hxs = response.body.decode('utf-8')
        hjson = json.loads(hxs)
        hjson2 = hjson['data']
        for lis in hjson2['vlist']:
            url = "https://api.bilibili.com/x/web-interface/view?aid=" + str(lis['aid'])
            yield scrapy.Request(url=url, headers=headers, method='GET', callback=self.parse2,meta={'title': str(lis['title'])})

    def parse2(self,response):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        hxs = response.body.decode('utf-8')
        hjson = json.loads(hxs)
        title = response.meta['title']
        url = "https://api.bilibili.com/x/v1/dm/list.so?oid=" + str(hjson['data']['cid'])
        yield scrapy.Request(url=url, headers=headers, method='GET', callback=self.parse3,meta={'cid': str(hjson['data']['cid']),'aid':str(hjson['data']['aid']),'title': title})

    def parse3(self, response):
        selector = Selector(text = response.body)
        l = selector.xpath('//d/text()').extract()
        for ll in l:
            item = BilibiliTMItem()
            item["tanmu"] = ll
            item["title"] = response.meta['title']
            item["aid"] = response.meta['aid']
            item["cid"] = response.meta['cid']
            yield item