import scrapy
import re
import time
from scrapy.crawler import CrawlerProcess
import requests
from ..items import BaiduItem
class BaiduSpider(scrapy.Spider):
    name = "Baidu_01"
    start_urls = ["https://top.baidu.com/board?tab=realtime"]
    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Cookie':'BAIDUID=E48F6AC74081CDCF935C91292FA4F74E:FG=1; BIDUPSID=E48F6AC74081CDCF935C91292FA4F74E; PSTM=1566041524; BAIDUID_BFESS=E48F6AC74081CDCF935C91292FA4F74E:FG=1; COOKIE_SESSION=375769_1_4_9_2_6_0_1_4_5_0_0_11398948_0_0_0_1709003742_1697553890_1709379501%7C9%23129165529_10_1697542719%7C4; jsdk-uuid=32dc8ee9-772f-4c01-9222-ab1c6ec05f3d; BD_UPN=123253; BAIDU_WISE_UID=wapp_1710939865663_270; ZFY=XLv:B9nSbAmQOU:B2ft7cHLdAFu6GnpL41VuK4jhPUXkw:C; BA_HECTOR=0ga10h8001a58h2l2484a08lfr6s2p1j072541t; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[C0p6oIjvx-c]=mbxnW11j9Dfmh7GuZR8mvqV; H_PS_PSSID=40080_40373_40415_40465_40458_40317_40510_40398_60045_60029_60032_60046_60059; delPer=0; BD_CK_SAM=1; PSINO=3; BDSVRTM=211; kleck=ea91c2ede4b49058166b24b975cae3c1',
            'Host':'www.baidu.com',
        }
        for url in self.start_urls:
            r = requests.get(url, headers=headers,allow_redirects=False)
            if r.status_code == 200:
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)
            else:
                print(f"r.headers = {r.headers['Location']}")
                yield scrapy.Request(r.headers['Location'], callback=self.parse, dont_filter=True,headers=headers)

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Cookie':'BAIDUID=E48F6AC74081CDCF935C91292FA4F74E:FG=1; BIDUPSID=E48F6AC74081CDCF935C91292FA4F74E; PSTM=1566041524; BAIDUID_BFESS=E48F6AC74081CDCF935C91292FA4F74E:FG=1; COOKIE_SESSION=375769_1_4_9_2_6_0_1_4_5_0_0_11398948_0_0_0_1709003742_1697553890_1709379501%7C9%23129165529_10_1697542719%7C4; jsdk-uuid=32dc8ee9-772f-4c01-9222-ab1c6ec05f3d; BD_UPN=123253; BAIDU_WISE_UID=wapp_1710939865663_270; ZFY=XLv:B9nSbAmQOU:B2ft7cHLdAFu6GnpL41VuK4jhPUXkw:C; BA_HECTOR=0ga10h8001a58h2l2484a08lfr6s2p1j072541t; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[C0p6oIjvx-c]=mbxnW11j9Dfmh7GuZR8mvqV; H_PS_PSSID=40080_40373_40415_40465_40458_40317_40510_40398_60045_60029_60032_60046_60059; delPer=0; BD_CK_SAM=1; PSINO=3; BDSVRTM=211; kleck=ea91c2ede4b49058166b24b975cae3c1',
            'Host':'www.baidu.com',
        }
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
            item['Origin']='Baidu'
            item['Topic']=topic
            yield scrapy.Request(url=searched_url, callback=self.parse_urls,meta={'item':item},headers=headers)

    def parse_urls(self,response):
        print(f"Success enter {response.meta['item']['Topic']}")
        item=response.meta['item']
        for each in response.xpath("//div[@srcid='200']"):
            detailed_url=each.xpath("./div/h3/a/@href")[0].extract()#各个搜索结果的URL
            item['Url']=detailed_url
            item['Abstract']=each.xpath("./div/div/div/span[2]/@aria-label")[0].extract()
            item["Author"]=each.xpath("./div/div/div/div/a/span/text()")[0].extract()
            item['Comment']=''
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