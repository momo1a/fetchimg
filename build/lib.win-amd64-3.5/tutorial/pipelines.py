# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.contrib.pipeline.images import ImagesPipeline

class TutorialPipeline(ImagesPipeline):
    
    def open_spider(self, spider):
        self.file = open('items.json', 'a')

    def close_spider(self, spider):
        self.file.close()
        
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
    
    # 请求图片地址 下载图片
    def get_media_requests(self, item, info):
        for image_url in item['imgs']:
            yield scrapy.Request(image_url)
    
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
