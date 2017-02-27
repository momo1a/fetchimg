# coding:utf-8
import scrapy
from scrapy.spiders import CrawlSpider, Rule
import json
from scrapy.mail import MailSender
from scrapy.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse, Request
from scrapy.loader import ItemLoader
from tutorial.items import TutorialItem
import re

class MySpider(CrawlSpider):
    name = 'mm131'
    allowed_domains = ['mm131.com']
    start_urls = ['http://www.mm131.com']

    rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        # Rule(LinkExtractor(allow=('\w+$', ), deny=('subsection\.php', ))),

        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        # Rule(LinkExtractor(allow=('xinggan','qingchun$','xiaohua$','chemo$','qipao$','mingxing$' )), callback='parse_item'),
    )

    def parse(self, response):
        # self.log('Hi, this is an item page! %s' % response.url)
        urls = response.xpath('//div[@class="nav"]/ul/li/a[re:test(@href,"' + self.start_urls[0] + '/\w+")]/@href').extract()
           #    response.xpath('//div[@class="nav"]/ul/li/a[re:test(@href,"http://www.mm131.com/\w+")]/@href').extract()
         
        for url in urls:
            yield Request(url, callback=self.caterogy_parse)
            
        # item = scrapy.Item()
        # item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        # item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        # item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        # return item
    
    # 分类页解析器    
    def caterogy_parse(self, response):
        try:
            detail_url = response.xpath('//dl[contains(@class,"list-left public-box")]/dd/a[re:test(@href,"' + self.start_urls[0] + '/\w+/\d+\.html")]/@href').extract()
            # self.log('current request url:'+response.url)
            
            for url in detail_url:
                # 请求到当前分类的第一页所有详情页url
                yield Request(url,callback=self.detail_parse)
                                 
            # 下一页
            current_url = re.findall(r'http://www.mm131.com/\w+/', response.url)[0]
            # 获取到下一页的url     
            next_url = response.xpath('//dd[@class="page"]/a[text()="下一页"]/@href').extract()[0]
            
            return Request(current_url + next_url, callback=self.caterogy_parse)
        except Exception as e:
            pass
            
    # 详情页解析器 获取数据
    def detail_parse(self, response):    
        try:
            item = TutorialItem()
             
            title = response.xpath('//title/text()').extract()[0][:-19]
            # l.add_value('title', title[:-14]) 
            # return l.load_item()
            # self.log(response.url)
            img_src = response.xpath('//div[@class="content-pic"]/a/img/@src').extract()[0]
            # 图片所属id
            mmid = img_src.split('/')[-2]
            imgs = response.meta.get('item')
            if imgs:
                imgs = imgs
            else :
                imgs = []
            imgs.append(img_src)
            detail_current_url = re.findall(r'http://www.mm131.com/\w+/', response.url)[0]
            detail_next_page = response.xpath('//div[@class="content-page"]/a[text()="下一页"]/@href').extract()
            if detail_next_page:  
                return Request(detail_current_url + detail_next_page[0], callback=self.detail_parse,meta={'item':imgs})
            else :
                self.log('over!!!!!!!!!!**************'+mmid)
                item['title']= title
                item['imgs'] = imgs
                item['mmid'] = mmid
                return item
        except Exception as e:
            self.log(e)    
            
            
                   
