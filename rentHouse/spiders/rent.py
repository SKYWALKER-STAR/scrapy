import re
import scrapy
import logging
from pathlib import Path
from rentHouse.items import RentItem


class RentSpider(scrapy.Spider):
    name    = "rent"
    logger  = logging.getLogger()

    def start_requests(self):
        urls = [
             "https://gz.zu.anjuke.com/?from=esf_list"
             #"https://bj.zu.anjuke.com/?from=esf_list"
             #"https://wh.zu.anjuke.com/?from=HomePage_TopBar"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = RentItem()
        div_list = response.css("div.zu-itemmod")

        pattern_1 = ".*\n.*"
        pattern_2 = "^\n"

        for i in div_list:

            tag_link    = i.css("div.zu-info h3 a::attr(href)")
            tag_title   = i.css("div.zu-info a b.strongbox::text")
            tag_price   = i.css("div.zu-side strong.price::text")
            tag_address = i.css("div.zu-info address.details-item a::text")
            tag_region  = i.css("div.zu-info address.details-item::text")

            link    = tag_link.get()
            title   = tag_title.get()
            price   = tag_price.get()
            address = tag_address.get()

            detail_btag      = i.css("div.zu-info p.bot-tag")

            detail_tag_d      = i.css("div.zu-info p.tag")
            detail_tag_t      = i.css("div.zu-info p.tag::text")

            #--------------------------------#
            #处理div.zu-info p.bot-tag中的内容#
            #--------------------------------#
            flag = 0
            for i in detail_btag:
                rv = i.css('span::text')
                basicInfo = {'1':'','2':'','3':'','4':''}
                count = 1
                for j in rv:
                    basicInfo[str(count)] = j.get()
                    count += 1

            #--------------------------------#
            #处理div.zu-info p.tag中的内容   #
            #--------------------------------#

            s = ""
            for j in detail_tag_t:
                if j.get() != " ":
                    s = s + ':' + j.get()
                else:
                    continue
            sList = s.split(':')
            sList = [item for item in filter(lambda x:re.match(pattern_1,x) == None and x != '',sList)]

            detail_tag_dList = []
            for j in detail_tag_d:
                i = j.css("b.strongbox::text")
                for m in i:
                    detail_tag_dList.append(m.get())

            li_tag = []
            for i in range(0,len(detail_tag_dList)):
                li_tag.append(detail_tag_dList[i])
                li_tag.append(sList[i])


            #--------------------------------#
            #处理div.zu-info address中的内容 #
            #--------------------------------#
            li_region = []
            for i in tag_region:
                li_region.append(i.get())

            li_region = [item for item in filter(lambda x:re.match(pattern_2,x) == None,li_region)]

            item['A']      = title
            item['B']      = price
            item['C']      = address
            item['D']      = basicInfo['1']
            item['E']      = basicInfo['2']
            item['F']      = basicInfo['3']
            item['G']      = basicInfo['4']
            item['H']      = "".join(li_tag)
            item['I']      = "".join(li_region).strip()
            item['J']      = link

            yield item
        next_page  = response.css("div.multi-page a.aNxt::attr(href)").get()
        if next_page is not None:
           yield response.follow(next_page, callback=self.parse)
