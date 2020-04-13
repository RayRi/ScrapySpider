#-*-coding:utf8-*-
from __future__ import absolute_import

import logging
import scrapy

from functools import partial, wraps
from ScrapyFrame.utils.base import database
from ScrapyFrame.utils.base.exceptions import *


class EndsPipeline:
    """Open And Close End Pipeline
    
    Define item Store pipelines, but just about open_spider and close_spider. 

    Properties:
        _logger: logger object, specify it's pipeline LoggerAdapter
        log: method that can log information
        open_spider: Pipeline method, when open spider, it's called
        close_spider: Pipeline mehtod, when close spider
        connect: a method create pymysql.connections.Connection object
    """
    def log(self, message, level=logging.DEBUG, **kwargs):
        """Run logger to display log information"""
        self._logger.log(level, message, **kwargs)


    def open_spider(self, spider):
        self._db = self.settings["db"]
        self._db_type = self.settings["db_type"]
        self._db_cache = self.settings["db_cache"]

        # connect cache database that is store some cache data, so that can check 
        # duplicated data, or do sth. else
        if self._db_cache == "redis":
            self.cache_conn = database.RedisConnect()
        else:
            raise NotSupported(f"Cache database {db_cache} can't be supported. "+
                                "Redis can be supported")


    def close_spider(self, spider):
        """Close Connections"""
        self.cache_conn.close()

    


class Middleware:
    """Middleware Base"""
    @property
    def _logger(self):
        """Logger Property"""
        NotImplemented
        

    def log(self, message, level=logging.DEBUG, **kwargs):
        """Run logger to display log information"""
        self._logger.log(level, message, **kwargs)



class SpiderBase(scrapy.Spider):
    """Spider Base"""
    @property
    def _logger(self):
        """Logger Property"""
        NotImplemented
        

    def log(self, message, level=logging.DEBUG, **kwargs):
        """Run logger to display log information"""
        self._logger.log(level, message, **kwargs)