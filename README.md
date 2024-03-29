# Some Tips about Srtp
### 目前存在两个问题:
1. ***BaiduSpider_02*** 在爬取网页时会经常性的遇到*302-Redirection* 问题，导致无法爬取全文。
2. ***WeiboSpider*** 要时常更新Cookie否则无法爬取微博评论
### March.13 Update:
1. 添加了start_project功能用于直接启动爬虫，需额外安装subprocess库。
2. 修复了部分***BaiduSpider*** *302-Redirection*爬取问题)(具体则是通过增加时间间隔实现)
3. 在爬取正文方面还有一些问题，需要进一步的调试。eg：百家号文章直接重定向到验证码页面，无法爬取。
### March.15 Update:
1. 修改了pipeline部分使其连接至本地mysql数据库
2. 修改了item以及spider中有关结构，使从百度和微博爬取的内容能够存入同一个数据库中
3. spider添加了start_url用于寻找重定向之前的url，为此需要安装requests库。
4. django添加了数据库直接连接至本地服务器。
### March.29 Update:
1. 前端大致页面搭建完毕，可以尝试运行。
2. Baidu_01中添加了host，可以尝试一下稳定性。
# 使用pipeline说明：
1. 需要额外安装pymysql库用于启动mysql
2. 在连接服务器时的host-ip需要变动，目前适用于连接本地服务器，若要连接远程服务器，需要将host-ip的值更改为远程服务器的ip地址。
3. 关于连接远程服务器，可参考
*blog：https://juejin.cn/post/7055884037327912967* 目前的username可以选择July，password为123456，而服务器的id由于局域网会有变化。
4. 更新了django连接本地数据库的配置，具体可参考: *https://blog.csdn.net/changyana/article/details/122790568*
