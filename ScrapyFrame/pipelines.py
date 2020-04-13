# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import json
import time

from ScrapyFrame.utils.base import EndsPipeline
from ScrapyFrame.utils.base import database


class MySQLPipeline(EndsPipeline):
    """MySQL Data Item Pipeline"""
    def __init__(self, settings=None):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        settings = settings
        return cls(settings=settings)


    def open_spider(self, spider):
        self._logger = logging.getLogger(__class__.__name__+"."+spider.name)
        super().open_spider(spider)
        self._db_type = "mysql"
        self.conn = database.MySQLConnect(db=self._db) 
        self.file = open(self.settings.get("LOG_FILE").replace(".log", "error.csv"), "w")


    def process_item(self, item, spider):
        try:
            fields = self.settings.get("OPINION_FIELDS")
            table = self.settings.get("default_tb")
            sentence = self.insert_sentence(table, fields)
            data = []
            for field in fields:
                if isinstance(item.get(field), (str, float, int)):
                    data.append(item.get(field))
                elif isinstance(item.get(field), (list, tuple)):
                    data.append("\t".join(item.get(field)))
                else:
                    data.append(None)
                

            self.conn.cursor.execute(sentence, data)
            self.conn.Connection.commit()
            self.log(f"Insert {table} Successful", level=logging.INFO)
        except Exception as err:
            self.file.write(json.dumps(dict(item, error_reason=err), ensure_ascii=False)+ "\n")
            self.log(f"Insert Failed resson {err}, address {item['url']}", level=logging.CRITICAL)
        return item


    def close_spider(self, spider):
        super().close_spider(spider)
        self.conn.close()
        self.file.close()


    def insert_sentence(self, table, fields, symbol=r"%s"):
        """Create SQL insert sentence
        Create a insert sentence, like that:
            INSERT INTO <table> (`col1`, `col2`) VALUES (%s, %s)
        """
        sentence = """
            INSERT INTO {tb} {fieldnames} VALUES {values_symbol};
        """

        fieldnames = "({column})".format(
            column=",".join("`{}`".format(field) for field in fields)
        )

        values_symbol = "(" + ",".join((symbol for i in range(len(fields)))) + ")"

        sentence = sentence.format(
            tb=table, fieldnames=fieldnames, values_symbol=values_symbol
        )

        return sentence


class MongoDBPipeline(EndsPipeline):
    """MongoDB Pipeline"""
    def __init__(self, settings=None):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        settings = settings
        return cls(settings=settings)


    def open_spider(self, spider):
        super().open_spider(spider)
        self._logger = logging.getLogger(__class__.__name__+"."+spider.name)
        self.conn = database.MongoDBConnect(db=self._db)
        self.database = self.conn.database
        self.file = open(self.settings.get("LOG_FILE").replace(".log", "error.csv"), "w")


    def process_item(self, item, spider):
        try:
            collections = self.database[self.settings.get("default_tb")]
            item["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item["update_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            insert_ = collections.insert_one(dict(item))

            if insert_.inserted_id:
                self.log(f"Insert collections {collections.name} successful", level=logging.INFO)
            else:
                self.log(f"Insert collections {collections.name} failed, maybe duplicated: {item}", \
                    level=logging.DEBUG)
        except Exception as err:
            self.file.write(json.dumps(dict(item, error_reason=err), ensure_ascii=False)+ "\n")
            self.log(f"Insert Failed resson {err}, address {item['url']}", level=logging.CRITICAL)

        return item

    
    def close_spider(self, spider):
        super().close_spider(spider)
        self.conn.close()
        self.file.close()