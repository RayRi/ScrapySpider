# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from ScrapyFrame.utils.base import EndsPipeline
from ScrapyFrame.utils.base import database

class MySQLPipeline(EndsPipeline):
    """MySQL Data Item Pipeline"""
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        cls.settings = settings
        return cls


    def open_spider(self, spider):
        super().open_spider(self, spider)
        self._db_type = "mysql"
        self.conn = database.MySQLConnect(db=self._db) 


    def process_item(self, item, spider):
        return item


    def close_spider(self, spider):
        super().close_spider(self, spider)
        self.conn.close()


class MongoDBPipeline(EndsPipeline):
    """MongoDB Pipeline"""
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        cls.settings = settings
        return cls


    def open_spider(self, spider):
        super().open_spider(self, spider)
        self.conn = database.MongoDBConnect(db=self._db)


    def process_item(self, item, spider):
        return item

    
    def close_spider(self, spider):
        super().close_spider(self, spider)
        self.conn.close()