# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import time
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.contrib.spiders import Spider
import requests
from scrapy.utils.project import get_project_settings
import os
class TutorialPipeline(ImagesPipeline):
    
    def open_spider(self, spider):
        #self.file = open('items.json', 'a')
        pass

    def close_spider(self, spider):
        #self.file.close()
        pass
        
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item)) + "\n"
#         self.file.write(line)
#         return item
    
     
    def process_item(self, item, spider):
        if 'imgs' in item:#如何‘图片地址’在项目中
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
        return item