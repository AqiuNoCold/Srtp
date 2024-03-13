# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import time
import scrapy
import scrapy.http
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class BaiduSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self):
        # 使用无头浏览器访问
        self.options = Options()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.wait = WebDriverWait(self.driver, 10)

    def __del__(self):
        self.driver.close()

    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(1)
        return scrapy.http.HtmlResponse(url=request.url, body=self.driver.page_source, encoding='utf-8',
                                        request=request, status=200)
