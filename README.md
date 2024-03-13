# Some Tips about Srtp
### 目前存在两个问题:
1. ***BaiduSpider_02*** 在爬取网页时会经常性的遇到*302-Redirection* 问题，导致无法爬取全文。
2. ***WeiboSpider*** 要时常更新Cookie否则无法爬取微博评论
### March.13 Update:
1. 添加了start_project功能用于直接启动爬虫
2. 修复了部分***BaiduSpider*** *302-Redirection*爬取问题)(具体则是通过增加时间间隔实现)
3. 在爬取正文方面还有一些问题，需要进一步的调试。eg：百家号文章直接重定向到验证码页面，无法爬取。