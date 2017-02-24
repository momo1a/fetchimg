# coding:utf-8
import scrapy
from scrapy.spiders import CrawlSpider, Rule
import json
from scrapy.mail import MailSender
from scrapy.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse,Request
from scrapy.loader import ItemLoader
from tutorial.items import TutorialItem
import re
from twisted.python.compat import items

class MyDetailSpider(CrawlSpider):
    name = 'mm131_detail'
    allowed_domains = ['mm131.com']
    
    def __init__(self, category=None, *args, **kwargs):
        super(MyDetailSpider, self).__init__(*args, **kwargs)
        file_obj = open('detail_url.txt','r')
        line = file_obj.readline()
        while line:
            self.start_urls.append(line.strip('\n') )
            line = file_obj.readline()
        file_obj.close()

    def parse(self,response):    
        try:    
            item = TutorialItem()

            title = response.xpath('//title/text()').extract()[0][:-19]
            #l.add_value('title', title[:-14]) 
            #return l.load_item()
            #self.log(response.url)
            self.log(title)
            img_src = response.xpath('//div[@class="content-pic"]/a/img/@src').extract()[0]
            #图片所属id
            #mmid = img_src.split('/')[-2]
            imgs = response.meta.get('item') 
            if imgs:
                imgs = imgs
            else:
                imgs = []
            imgs.append(img_src)
             
            #imgs.append(img_src)
             
            #item['title'] = title
            #item['imgs'] =  img_src
            
#             file_object = open('src.txt', 'a')
#             file_object.write(img_src+'\n')
#             file_object.close()
            detail_current_url = re.findall(r'http://www.mm131.com/\w+/', response.url)[0]
            detail_next_page = response.xpath('//div[@class="content-page"]/a[text()="下一页"]/@href').extract()
             
            if detail_next_page: 
                yield Request(detail_current_url + detail_next_page[0],callback=self.parse,meta={'item':imgs})
                
            else :
                
                self.log('!!!!!!!!!*************************!!!!!!!!!!!!!!!!!')
                item['imgs'] = imgs
                item['title'] = title
                 
                yield item
        except Exception as e:
            self.log(e)    
            
                
                   