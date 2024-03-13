import scrapy
import re
import time
from scrapy.crawler import CrawlerProcess
from ..items import BaiduItem
class BaiduSpider(scrapy.Spider):
    name = "Baidu_01"
    start_urls = ["https://top.baidu.com/board?tab=realtime"]

    def parse(self, response):
        Topics = []
        for each in response.xpath("//div[@class='c-single-text-ellipsis']"):
            topic=each.xpath("./text()")[0].extract()
            topic=re.sub("\s+", "", topic)#这里处理后得到的就是标题
            Topics.append(topic)
            pre_url='https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word='
            searched_url=pre_url+topic#这里的是对标题进行搜索后得到的网页的url
            #print(searched_url)
            #print(topic)
            item=BaiduItem()
            item['Baidu_Topic']=topic
            yield scrapy.Request(url=searched_url, callback=self.parse_urls,meta={'item':item})

    def parse_urls(self,response):
        print(f"Success enter {response.meta['item']['Baidu_Topic']}")
        item=response.meta['item']
        for each in response.xpath("//div[@srcid='200']"):
            detailed_url=each.xpath("./div/h3/a/@href")[0].extract()#各个搜索结果的URL
            item['Baidu_Url']=detailed_url
            item['Abstract']=each.xpath("./div/div/div/span[2]/@aria-label")[0].extract()
            item["Author"]=each.xpath("./div/div/div/div/a/span/text()")[0].extract()
            yield item
            # yield scrapy.Request(url=detailed_url, callback=self.parse_detail,meta={'item':item})

    # def parse_detail(self,response):
    #     item=response.meta['item']
    #     print(f"调用成功{item['Abstract']}")
    #     abstract = item["Abstract"][4:10]
    #     print(abstract)
    #     text = ""
    #     for each in response.xpath(f'//p[contains(text(),"{abstract}")]/parent::*/parent::*//p'):
    #         print("开始输出")
    #         com = each.xpath('text()').extract()
    #         if not com:
    #             continue
    #         else:
    #             text = text + com[0]
    #     print(text)
    #     item["Comment"] = text
    #     if item["Comment"]  != "":
    #         yield item
    #     else:
    #         yield scrapy.Request(url=item["Baidu_Url"], callback=self.parse_detail,meta={'item':item})