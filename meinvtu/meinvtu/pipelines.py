# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy, os, requests, pymongo, time


class MeinvtuPipeline(object):
    def process_item(self, item, spider):
        for file_name in item['atlas_names']:
            dir_path = 'G:/学习/github/scrapy_learning/meinvtu/image/%s/' % file_name

            '''if not os.path.exists(dir_path):
                os.makedirs(dir_path)'''
        return item


class MongoDBPipeline(object):
    def __init__(self):
        try:
            connect = pymongo.MongoClient(host='localhost', port=27017)
        except:
            print('Datebase is busying.....')
            time.sleep(2)
            connect = pymongo.MongoClient(host='localhost', port=27017)
        db = connect['spiders']
        self.collection = db['meinvtu']
        self.collection.drop()

    def process_item(self, item, spider):
        info = dict(item)
        self.collection.insert(info)
        return item
