from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

from douban_spider.items import DoubanSpiderItem
http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=2&bidSort=&buyerName=&projectId=&pinMu=&bidType=7
&dbselect=bidx&kw=&start_time=2017%3A01%3A24&end_time=2018%3A01%3A24&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName=

http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=22697&bidSort=&buyerName=&projectId=&pinMu=&bidType=7
&dbselect=bidx&kw=&start_time=2017%3A01%3A24&end_time=2018%3A01%3A24&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName=


class DoubanSpider(CrawlSpider):
    name = "douban_many_movie_spider"
    download_delay = 1
    allowed_domains = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

    start_urls=['http://movie.douban.com/top250?start=0&filter=&type=']
    rules = (Rule(LinkExtractor(allow=(r'http://movie\.douban\.com/top250\?start=\d+&filter=&type=')),callback='parse_item',follow=True),)
    
    def parse_item(self,response):
        print response
        sel=Selector(response)
        item=DoubanSpiderItem()
        soup=BeautifulSoup(response.url.text,'lxml')
        movie_name=sel.xpath('//span[@class="title"][0]/text()').extract()
        star=sel.xpath('//span[@class="rating_num"]/text()').extract()
        quote=soup.find_all('p',class_='quote').find('span',class_='inq').text()
        
        item['movie_name']=[n.encode('utf-8') for n in movie_name]
        item['star']=[n for n in star]
        item['quote']=[n.encode('utf-8') for n in quote]
        
        yield item