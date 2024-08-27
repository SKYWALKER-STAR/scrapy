# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import csv
from itemadapter import ItemAdapter
from rentHouse.items import RentItem


class RentPipelines(object): 

    def __init__(self):

        headers = ('A','B','C','D','E','F','G','H','I','J')
        

        self.f = open('rent.csv','w+',encoding='utf-8',newline='')

        self.f_csv = csv.DictWriter(self.f,headers)

        self.f_csv.writeheader()

        pass

    def process_item(self, item, spider):

        self.f_csv.writerow(item)
        return item

    def close_spider(self,spider):
        self.f.close()
