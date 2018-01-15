# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from scrapy.selector import HtmlXPathSelector
# from scrapy.http import Request
# from urllib.request import urlopen
from scrapy.http import Request
# from hello.items import ZhaopinItem
# from scrapy.spiders import CrawlSpider, Rule
from time import sleep
# from scrapy.linkextractors import LinkExtractor
from lxml import etree
import pymongo
from bson.objectid import ObjectId
import re
client = pymongo.MongoClient(host="127.0.0.1")
db = client.publicHealth # 库名dianping
collection = db.healthTitle
import redis  # 导入redis数据库
r = redis.Redis(host='127.0.0.1', port=6379, db=0)
ii = 0

class healthClassSpider(scrapy.Spider):
    name = "health3"
    allowed_domains = ["ys137.com"]  # 允许访问的域

    def __init__(self):
        # global pid
        # 查询reids库novelurl
        #qidianNovelSpider.start_urls=["https://read.qidian.com/chapter/kbE0tc0oVoNrZK4x-CuJuw2/92LFs_xdtPXwrjbX3WA1AA2",]
        start_urls = []
        urlList = r.lrange('titlenameurl', 0,1)
        ii = 0
        self.dict = {}
        for item in urlList:
            itemStr = str(item, encoding="utf-8")
            arr = itemStr.split(',')
            classid = arr[0]
            pid = arr[1]
            url = arr[2]
            print(arr[2])
            start_urls.append(url)
            self.dict[url] = {"classid": classid, "pid": pid, "num": 0}
            ii += 1
            if ii > 1:
                break
        print(start_urls)
        self.start_urls = start_urls

    def parse(self, response):
        classInfo = self.dict[response.url]
        objectid = classInfo['classid']
        objectid2 = ObjectId(objectid)
        pid = classInfo['pid']
        num = classInfo['num']
        ii = ""
        #==================================================================================
        hxs = HtmlXPathSelector(response)
        hxsObj = hxs.select('//div[@class="article-content"]/table/tr/td/p')
        for secItem in hxsObj:
            healthTitleContent = secItem.select('text()').extract()
            #print(healthTitleContent[0])
            if healthTitleContent ==[]:
                pass
            else:
                ii = ii+healthTitleContent[0]
        print(ii)
                # db.healthTitle.update({"_id": objectid2}, {"$set": {'healthTitleContent':ii}})
        # sleep(0.3)
        print('------------------------------------------------------')
        '''
        html = response.body.decode('gbk')
        selector = etree.HTML(html)
        Name = selector.xpath('//div[@class="article-content"]/table/tr/td/h2/text()')
        #print(Name)
        # print(len(Name))
        arr=[]
        for i in range(len(Name)):
            print(Name[i])
            arr[i]=Name[i]+'/n'
        #db.healthTitle.update({"_id": objectid2}, {"$set": {'healthTitlechapter': Name}})
        # print('----------------------------------------------------')

        classname = selector.xpath('//div[@class="article-content"]/table/tr/td/p/text()')
        #print(classname)
        for a in range(len(classname)):
            print(classname[a])


       # db.healthTitle.update({"_id": objectid2}, {"$set": {'healthTitleContent': classname}})
'''
