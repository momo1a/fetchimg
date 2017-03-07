from scrapy.spiders import CrawlSpider
from scrapy.http import Request
import json
# 天极蜘蛛
class YeskySpider(CrawlSpider):
    name = 'yesky'
    allowed_domains = ['yesky.com']
    start_urls = ['http://pic.yesky.com/c/6_20491.shtml']
    
    def parse(self, response):
        
        urls = response.xpath('//div[@class="lb_box"]/dl/dt/a/@href').extract()
        self.log(urls)
        for url in urls:
            #file_obj =  open('yesky_detail_urls.txt','a')
            #file_obj.write(url+'\n')
            #file_obj.close()
            yield Request(url,callback=self.detail_parse)
            
        next_url = response.xpath('//div[@class="flym"]/font/a[text()="下一页"]/@href').extract()
        if next_url:
                self.log('http://pic.yesky.com' + next_url[0])
                yield Request('http://pic.yesky.com' + next_url[0], callback=self.parse)
    
    def detail_parse(self,response):
        #img_src = response.xpath('//div[@class="l_effect_img_mid"]/a/img/@src').extract()[0]
                     
        detail_urls =  response.xpath('//div[@class="overview"]/ul/li/a/@href').extract()
        i = 0
        for url in detail_urls:
            yield Request(url,callback=self.detail_sub_parse,meta={'index':i})
            i = i+1
            
              
    def detail_sub_parse(self,response):
               
        index = response.meta.get('index')
        imgs = []
        img_src = response.xpath('//div[@class="l_effect_img_mid"]/a/img/@src').extract()[0]
        if index != 0:
            imgs.append(img_src)
        file_obj =  open('index.txt','a')
        file_obj.write(json.dumps(imgs)+'\n')
        file_obj.close()
         
            
            
        
               
               