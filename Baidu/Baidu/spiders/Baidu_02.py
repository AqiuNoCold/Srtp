import scrapy
from ..items import BaiduItem
import time
import json
class ZixunSpider(scrapy.Spider):
    name = "Baidu_02"
    start_urls = []

    def start_requests(self):
        with open("test.json", "r", encoding="utf-8") as f:
            dicts = json.load(f)
            for dic in dicts:
                item = BaiduItem()
                item["Baidu_Topic"] = dic["Baidu_Topic"]
                item["Baidu_Url"] = dic["Baidu_Url"]
                item['Abstract']=dic['Abstract']
                item['Author']=dic['Author']
                yield scrapy.Request(url=item['Baidu_Url'], callback=self.parse, meta={'item':item})
    def parse(self, response):
        item = response.meta['item']
        abstract = item["Abstract"][4:10]
        text = ""
        for each in response.xpath(f'//p[contains(text(),"{abstract}")]/parent::*/parent::*//p'):
            com = each.xpath('text()').extract()
            if not com:
                continue
            else:
                text = text + com[0]
        item["Comment"] = text
        print("item输出")
        print(item["Comment"])
        if item["Comment"] != "":
            yield item
        else:
            print("重新加载请求")
            yield scrapy.Request(url=item["Baidu_Url"], callback=self.Retry_parse, meta={'item':item,'retry_time':0},dont_filter=True)

    def Retry_parse(self, response):
        print("成功调用")
        item = response.meta['item']
        retry_time = response.meta['retry_time']+1
        if item["Comment"] == "":
            if retry_time>3:
                item['Comment'] = "实在抓不下来"
                yield item
            else:
                print(f"Retry time: {retry_time}")
                request = scrapy.Request(url=item["Baidu_Url"], callback=self.Retry_parse, meta={'item':item,'retry_time':retry_time})
                request.dont_filter = True
                yield request
        else:
            print("item输出2")
            yield item