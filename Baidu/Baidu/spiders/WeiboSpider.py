# import sys
import scrapy
import re
import requests
from scrapy.crawler import CrawlerProcess

# sys.path.append(r"WeiboSpider\WeiboSpider")

from ..items import  WeibospiderItem
class WeiboSpider(scrapy.Spider):
    name = "Weibo"
    allowed_domains = ["s.weibo.com"]
    start_urls = ["https://s.weibo.com/top/summary?cate=socialevent"]
    def start_requests(self):
        headers = {
            "Cookie": "SINAGLOBAL=802098472984.5715.1697621151360; _s_tentry=passport.weibo.com; Apache=7217574065072.632.1708774393705; ULV=1708774393716:5:1:1:7217574065072.632.1708774393705:1700046431628; XSRF-TOKEN=q90O1pJU6deXYnXkmzWhvAiN; PC_TOKEN=af130cdd6c; appkey=; WBtopGlobal_register_version=2024022419; ALF=1711366767; SUB=_2A25I3aU_DeRhGeFL7VIW8ijMyz2IHXVrkrj3rDV8PUJbkNAGLUn9kW1NffXLbGl9FU7J0L7Iqb-6Ecl88fq-HBar; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhuGqs2PYQhXTjPjrjDRdMk5JpX5o275NHD95QNSKq7S0zceh5pWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS0-cehMESo57eBtt; WBPSESS=d-XWAcJ2m95Bmfa1ESu0JOq9aDt83CMnNFDmbjCSj5MdAscFqXebj4Yc0wWr9nx0YITY-Fnl9eCTK3iXnnXfy4ZRxM6hPnI_f_eBPBuFnnSJO3Fii21XW7Ei6dMzhDvGjUrkDlpRfJ5NbvBmat55gg==; UOR=,,tophub.today",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        for url in self.start_urls:
            r = requests.get(url, headers=headers,allow_redirects=False)
            if r.status_code == 200:
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)
            else:
                print(f"r.headers = {r.headers['Location']}")
                yield scrapy.Request(r.headers['Location'], callback=self.parse, dont_filter=True)
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