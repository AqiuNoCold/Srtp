# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class BaiduPipeline:
    def __init__(self):
        self.connect = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='$wyh666$',
            db='spider'
        )
        self.cursor=self.connect.cursor()
    def process_item(self, item, spider):
        insert_sql ="INSERT INTO spider_db(Topic,Origin,Author,Abstract,Comment,Url) VALUES (%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(insert_sql,(item['Topic'],item['Origin'],item['Author'],item['Abstract'],item['Comment'],item['Url']))
        self.connect.commit()
        print(f"插入数据成功")
    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()