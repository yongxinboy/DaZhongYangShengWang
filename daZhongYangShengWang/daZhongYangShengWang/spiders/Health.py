import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
# from urllib.request import urlopen
from scrapy.http import Request
# from hello.items import ZhaopinItem
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
from urllib.request import urlopen
#from urllib.request import Request
from bs4 import BeautifulSoup
from lxml import etree
from bson.objectid import ObjectId

import pymongo
client = pymongo.MongoClient(host="127.0.0.1")
db = client.publicHealth          #库名dianping
collection = db.healthClass
import redis
r = redis.Redis(host='127.0.0.1', port=6379, db=0)


class healthClassSpider(scrapy.Spider):
    name = "health"
    allowed_domains = ["ys137.com"]  # 允许访问的域
    start_urls = [
        "https://www.ys137.com/lvyou/",
    ]

    #每爬完一个网页会回调parse方法
    # def parse(self, response):
    #     print(response.body.decode('utf-8'))
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        hxsObj = hxs.select('//div[@class="container-fluid top-nav"]/div[@class="container main clearfix"]/table[@class="pull-left"]/tr/th/a')
        for secItem in hxsObj:
            className = secItem.select('text()').extract()
            classUrl = secItem.select('@href').extract()
            print(className[0])
            print(classUrl[0])
            print('----------------------------------')

            classid = self.insertMongo(className[0], None)
            request = Request(classUrl[0], callback=lambda response, pid=str(classid): self.parse_subClass(response, pid))
            yield request
            print("======================")

    def parse_subClass(self, response, pid):
        hxs = HtmlXPathSelector(response)
        hxsObj = hxs.select('//div[@class="channel-sons pull-left"]/a')
        for secItem in hxsObj:
            className2 = secItem.select('text()').extract()
            classUrl2 = secItem.select('@href').extract()
            print(className2)
            print('----------------------------')
            print(classUrl2)
            classid = self.insertMongo(className2[0], ObjectId(pid))
            self.pushRedis(classid, pid, classUrl2[0])

    def insertMongo(self, classname, pid):
        classid = collection.insert({'classname': classname, 'pid': pid})
        return classid

    def pushRedis(self, classid, pid, url):
        healthurl = '%s,%s,%s' % (classid, pid, url)
        r.lpush('healthurl', healthurl)

