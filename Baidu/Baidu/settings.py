# Scrapy settings for Baidu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "Baidu"

SPIDER_MODULES = ["Baidu.spiders"]
NEWSPIDER_MODULE = "Baidu.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "Baidu (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16
# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Cookie":"SINAGLOBAL=802098472984.5715.1697621151360; _s_tentry=passport.weibo.com; Apache=7217574065072.632.1708774393705; ULV=1708774393716:5:1:1:7217574065072.632.1708774393705:1700046431628; XSRF-TOKEN=q90O1pJU6deXYnXkmzWhvAiN; PC_TOKEN=af130cdd6c; appkey=; WBtopGlobal_register_version=2024022419; ALF=1711366767; SUB=_2A25I3aU_DeRhGeFL7VIW8ijMyz2IHXVrkrj3rDV8PUJbkNAGLUn9kW1NffXLbGl9FU7J0L7Iqb-6Ecl88fq-HBar; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhuGqs2PYQhXTjPjrjDRdMk5JpX5o275NHD95QNSKq7S0zceh5pWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS0-cehMESo57eBtt; WBPSESS=d-XWAcJ2m95Bmfa1ESu0JOq9aDt83CMnNFDmbjCSj5MdAscFqXebj4Yc0wWr9nx0YITY-Fnl9eCTK3iXnnXfy4ZRxM6hPnI_f_eBPBuFnnSJO3Fii21XW7Ei6dMzhDvGjUrkDlpRfJ5NbvBmat55gg==; UOR=,,tophub.today",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}
# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   "Baidu.middlewares.BaiduSpiderMiddleware": 543,
}
LOG_LEVEL = 'ERROR'
# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "Baidu.middlewares.BaiduDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "Baidu.pipelines.BaiduPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
