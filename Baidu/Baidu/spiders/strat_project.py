import subprocess
subprocess.run(["scrapy","crawl","Baidu_01","-o","baidu.json"])
subprocess.run(["scrapy","crawl","Weibo","-o","weibo.json"])