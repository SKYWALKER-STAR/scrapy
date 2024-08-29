# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import csv
import pymysql
import datetime
from itemadapter import ItemAdapter
from rentHouse.items import RentItem


class RentPipelines(object): 

    def __init__(self):

        headers = ('A','B','C','D','E','F','G','H','I','J')
        

        self.f = open('rent.csv','w+',encoding='gb2312',newline='')

        self.f_csv = csv.DictWriter(self.f,headers)

        self.f_csv.writeheader()

        pass

    def process_item(self, item, spider):

        self.f_csv.writerow(item)
        return item

    def close_spider(self,spider):
        self.f.close()

class RentPipelinesMysql(object):
    def __init__(self):
        self.conn = pymysql.connect(
                host = '127.0.0.1',
                user = 'username',
                password = '********',
                database = 'scrapy_result'
        )

        self.cur = self.conn.cursor()

        self.timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def process_item(self,item,spider):
       #self.cur.execute(""" insert into rent_data_gz (title,price,name,rtype,direction,attr1,attr2,area,address) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(item['A'],item['B'],item['C'],item['D'],item['E'],item['F'],item['G'],item['H'],item['I']))
       self.cur.execute("""insert into rent_data_gz (title,price,name,rtype,direction,attr1,attr2,area,address,update_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE price=%s;""",(item['A'],item['B'],item['C'],item['D'],item['E'],item['F'],item['G'],item['H'],item['I'],self.timestr,item['B']))
       self.conn.commit()


    def close_spider(self,spider):
        self.cur.close()
        self.conn.close()
