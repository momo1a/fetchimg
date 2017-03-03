# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import time
from scrapy.pipelines.images import ImagesPipeline
from scrapy.spiders import Spider
import requests
from scrapy.utils.project import get_project_settings
import os
import pymysql
import logging
logger = logging.getLogger(__name__)

class TutorialPipeline(ImagesPipeline):
    
    def open_spider(self, spider):
        #self.file = open('items.json', 'a')
        self.conn = pymysql.connect(host='192.168.61.97',port=3306,user="root",passwd="123456",db="test",charset="utf8")
        self.cursor = self.conn.cursor()
         
        #pass

    def close_spider(self, spider):
        #self.file.close()
        self.conn.close()
        #pass
        
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item)) + "\n"
#         self.file.write(line)
#         return item
    
     
    def process_item(self, item, spider):
        if 'imgs' in item and spider.name == 'mm131':#如何‘图片地址’在项目中
            images = []#定义图片空集
            
            #dir_path = '%s/%s' % (get_project_settings()['IMAGES_STORE'], item['mmid'])
            dt = time.strftime('%Y/%m/%d',time.localtime(time.time()))
            dir_path = '%s/%s/%s' % ('lol',dt, item['mmid'])

            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for image_url in item['imgs']:
                us = image_url.split('/')[3:]
                image_file_name = '_'.join(us)
                file_path = '%s/%s' % (dir_path, image_file_name)
                images.append(file_path)
                if os.path.exists(file_path):
                    continue

                with open(file_path, 'wb') as handle:
                    response = requests.get(image_url, stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break

                        handle.write(block)

            item['imgs'] = images
            try:
                sql = 'INSERT INTO mm_imgs SET mmid="'+item['mmid']+'",img=\''+json.dumps(item['imgs'])+'\',title="'+item['title']+'",dateline= '+str(int(time.time()))
                logger.info(sql)
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                logger.info('ERROR ERROR ***** ERROR ERROR !!!'+e)
                self.conn.rollback()
                
        elif spider.name == 'yesky':
            
            pass
        
        
        return item
    
    