# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from bson.objectid import ObjectId
from movie_crawler.settings import MONGODB_COLLECTION, MONGODB_DB, MONGODB_HOST, MONGODB_PORT


class MovieCrawlerPipeline(object):

    def __init__(self):
        connection = MongoClient(
            MONGODB_HOST,
            MONGODB_PORT)
        self.db = connection[MONGODB_DB]
        self.collection = self.db[MONGODB_COLLECTION]

    def process_item(self, item, spider):
        self.collection.insert({"_id": ObjectId().__str__(),
                                'title': item['title'][0],
                                'content': item['content'][0],
                                'actors': item['actors'],
                                'detail': item['detail'][0],
                                'type': item['type'][0]})
        return item