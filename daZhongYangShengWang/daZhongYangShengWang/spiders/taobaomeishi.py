import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
# from urllib.request import urlopen
from scrapy.http import Request
# from hello.items import ZhaopinItem
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
from urllib.request import urlopen
# from urllib.request import Request
from bs4 import BeautifulSoup
from lxml import etree
from bson.objectid import ObjectId
from scrapy_splash import SplashRequest

ii = 0
class qidianClassSpider(scrapy.Spider):
    name = "taobao"
    allowed_domains = ["newrank.cn"]  # 允许访问的域
    start_urls = [
        "https://data.newrank.cn/articleResult.html?value=s&flag=true"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait':0.5})


    def parse(self, response):
        print(response.body.decode('utf-8'))
        '''
        hxs = HtmlXPathSelector(response)
        #hxsObj = hxs.select('//div[@class="title"]/a')
        secItem = hxs.select('//div[@class="search-result-boxout"]/div[@class="search-result-box search-result-box2"]')
        #for secItem in hxsObj:
        className = secItem.select('//div[@class="title"]/a/text()').extract()
        classUrl = secItem.select('//div[@class="title"]/a/@href').extract()
        price = secItem.select('//div[@class="price clearfix"]/a/em/text()').extract()
        print(className)
        print(classUrl)
        html = response.body.decode('utf-8')
        selector = etree.HTML(html)
        #adress = selector.xpath('//div[@class="price clearfix"]/a/ins/text()')
        adress = secItem.select('//div[@class="price clearfix"]/a/ins/text()').extract()
        count = secItem.select('//div[@class="saleinfo"]/a/em/text()').extract()

        print(price)
        print(adress)
        #ii += 1
        print(count)
'''