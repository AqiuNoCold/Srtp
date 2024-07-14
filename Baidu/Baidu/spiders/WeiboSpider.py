# import sys
import scrapy
import re
import requests
from scrapy.crawler import CrawlerProcess

# sys.path.append(r"WeiboSpider\WeiboSpider")

from ..items import  BaiduItem
class WeiboSpider(scrapy.Spider):
    name = "Weibo"
    allowed_domains = ["s.weibo.com"]
    start_urls = ["https://s.weibo.com/top/summary?cate=socialevent"]
    def start_requests(self):
        headers = {
            "Cookie": "SINAGLOBAL=802098472984.5715.1697621151360; UOR=,,tophub.today; ALF=1714024825; SUB=_2AkMRSZu8f8NxqwFRmfoTyGnhb4l_zADEieKnFWpnJRMxHRl-yT9kqmZbtRB6Osm1U1gC_14g9vQB28JneYc7myCM5gxA; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWu64-iny6mUVVVib2VQp1H; _s_tentry=passport.weibo.com; Apache=9115422418379.955.1712657549225; ULV=1712657549283:7:1:1:9115422418379.955.1712657549225:1710303190297; XSRF-TOKEN=tUva6TrKCY7xKHRg66QJSFTe; WBPSESS=V0zdZ7jH8_6F0CA8c_ussUNHjWHvGI6ggyrtP0cGSl5r66MUKWJlOwBdLGX9SeJKGtzgo3S08T7UESiNOISmlz4ydTeenR06DeYjA1AVq92e4cE2LuO1Tocbo-4JevQm",
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

        for each in Topic_urls:
            for i in range(1,4):
                full_topic_url = 'https://s.weibo.com'+each+"&page="+str(i)
                item = BaiduItem()
                item['Comment']=''
                item['Origin'] = 'Weibo'
                item['Abstract'] = 'none'
                item['Url'] = 'none'
                yield scrapy.Request(url=full_topic_url, callback=self.parse_topic,meta={'item':item})

        #scrapy crawl Weibo
    def parse_topic(self,response):
        Topic=response.xpath("//h1[@class='short']/a/text()")[0].extract()
        print(Topic)
        for each in response.xpath("//div[@action-type='feed_list_item'][@class='card-wrap']"):

            Author=each.xpath("div//a[@class='name']/text()")[0].extract()
            Text=each.xpath("div[2]/div[1]/div[2]/p[2]//text()").getall()
            if Text:
                pass
            else:
                Text=each.xpath("div[2]/div[1]/div[2]/p//text()").getall()
            if Text:
                Comment=''.join(Text)
                Comment=re.sub('[\n\s(收起)(展开)(\u200b)]', '', Comment)
                item = response.meta['item']
                item['Topic'] = Topic
                item['Author'] = Author
                item['Comment'] = Comment
                yield item


# from scrapy.utils.project import get_project_settings
#
# process = CrawlerProcess(get_project_settings())
# process.crawl(WeiboSpider)
# process.start()