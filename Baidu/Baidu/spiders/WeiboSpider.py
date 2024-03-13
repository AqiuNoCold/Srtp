# import sys
import scrapy
import re
from scrapy.crawler import CrawlerProcess

# sys.path.append(r"WeiboSpider\WeiboSpider")

from ..items import  WeibospiderItem
class WeiboSpider(scrapy.Spider):
    name = "Weibo"
    allowed_domains = ["s.weibo.com"]
    start_urls = ["https://s.weibo.com/top/summary?cate=socialevent"]

    def parse(self, response):
        Topic_urls =[]
        Topics = []
        for each in response.xpath("//td[@class='td-02']"):
            topic = each.xpath("a/text()")[0].extract()
            topic_url = each.xpath("a/@href")[0].extract()
            Topics.append(topic)
            Topic_urls.append(topic_url)

        #file=open('Topic_urls.txt','w',encoding='utf-8')
        #file.writelines(Topic_urls)
        #file.close()
        #print(Topic_urls)
        for each in Topic_urls:
            for i in range(1,4):
                full_topic_url = 'https://s.weibo.com'+each+"&page="+str(i)
                #print(full_topic_url)
                #print("Prepared")
                item = WeibospiderItem()
                item['Comment']=''
                yield scrapy.Request(url=full_topic_url, callback=self.parse_topic,meta={'item':item})

        #scrapy crawl Weibo
    def parse_topic(self,response):
        #print("Entered")
        Topic=response.xpath("//h1[@class='short']/a/text()")[0].extract()
        print(Topic)
        for each in response.xpath("//div[@action-type='feed_list_item'][@class='card-wrap']"):

            #print("Entered")
            Name=each.xpath("div//a[@class='name']/text()")[0].extract()
            #print(Name)
            Text=each.xpath("div[2]/div[1]/div[2]/p[2]//text()").getall()
            #div[2] / div[1] / div[2] / p[1]
            #div[2] / div[1] / div[2] / p[2]
            #print(each)
            if Text:
               # print("长：",Text)
                pass
            else:
                Text=each.xpath("div[2]/div[1]/div[2]/p//text()").getall()
                #print("短:", Text)
            #print(Text)
            if Text:
                Comment=''.join(Text)
                Comment=re.sub('[\n\s(收起)(展开)(\u200b)]', '', Comment)
                #print(Text)
                #print(Comment)
                #Name=each.xpath("div[2]/div[1]/div[2]/p/@nick-name").get()
                item = response.meta['item']
                item['Topic'] = Topic
                item['Name'] = Name
                item['Comment'] = Comment
                #print(item)
                yield item


# from scrapy.utils.project import get_project_settings
#
# process = CrawlerProcess(get_project_settings())
# process.crawl(WeiboSpider)
# process.start()