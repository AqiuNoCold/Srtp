# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Comment = scrapy.Field()
    Baidu_Topic=scrapy.Field()
    Baidu_Url=scrapy.Field()
    Abstract=scrapy.Field()
    Author=scrapy.Field()
    pass
class WeibospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Topic = scrapy.Field()
    Name = scrapy.Field()
    Comment = scrapy.Field()
    pass