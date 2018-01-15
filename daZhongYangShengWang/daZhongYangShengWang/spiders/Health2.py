# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector
# from scrapy.http import Request
# from urllib.request import urlopen
from scrapy.http import Request
# from hello.items import ZhaopinItem
# from scrapy.spiders import CrawlSpider, Rule
from time import sleep
# from scrapy.linkextractors import LinkExtractor

import pymongo
from bson.objectid import ObjectId
client = pymongo.MongoClient(host="127.0.0.1")
db = client.publicHealth  # 库名dianping
collection = db.healthTitle

import redis  # 导入redis数据库

r = redis.Redis(host='127.0.0.1', port=6379, db=0)

ii = 0


class healthClassSpider(scrapy.Spider):
    name = "health2"
    allowed_domains = ["ys137.com"]  # 允许访问的域

    def __init__(self):
        # global pid
        # 查询reids库novelurl
        # qidianNovelSpider.start_urls=["https://www.qidian.com/all",]
        start_urls = []
        urlList = r.lrange('healthurl', 0, 1)
        ii = 0
        self.dict = {}
        for item in urlList:
            itemStr = str(item, encoding="utf-8")
            arr = itemStr.split(',')
            classid = arr[0]
            pid = arr[1]

            url = arr[2]
            start_urls.append(url)
            self.dict[url] = {"classid": classid, "pid": pid,"urls":url, "num": 0}
            # ii += 1
            # if ii > 3:
            #     break
        print(start_urls)
        self.start_urls = start_urls

    def parse(self, response):
        classInfo = self.dict[response.url]
        objectid = classInfo['classid']
        pid = classInfo['pid']
        headurl=classInfo['urls']
        num = classInfo['num']
        if num > 3:
            return None
        hxs = HtmlXPathSelector(response)
        hxsObj = hxs.select('//div[@class="arc-infos clearfix"]/h2/a')
        for secItem in hxsObj:
            className = secItem.select('text()').extract()
            classUrl = secItem.select('@href').extract()
            print(className[0])
            print(classUrl)
            #classid =self.insertMongo(className[0],ObjectId(objectid))
            #self.pushRedis(classid,objectid, classUrl[0])

        #    --------------------------不用调用方法直接取下一页------------------------------------------------------------------------------
        nextPages= hxs.select('//ul[@class="pagination"]/li/a/@href')
        print(len(nextPages))
        nextPage=nextPages.extract()[len(nextPages)-1]
        #print(headurl)
        nextPage= headurl+nextPage
        #print(nextPage)
        classInfo['num'] += 1
        self.dict[nextPage] = classInfo
        request = Request(nextPage, callback=self.parse)
        yield request
        print('--------end--------------')
'''
    def insertMongo(self, className, pid):
        classid = collection.insert({'classname': className, 'pid': pid})
        return classid


    def pushRedis(self, classid, pid, classUrl):
        titlename = '%s,%s,%s,' % (classid, pid, classUrl)
        r.lpush('titlenameurl', titlename)
'''