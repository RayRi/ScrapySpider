#-*-coding:utf8-*-
"""
Description:
    The script is used to parse the configuration:
    * mysql, basic mysql database connection configuration
    * redis, basic redis database connection configuration. It's recommendation
        that use the connection pool 
"""
from __future__ import absolute_import

from pyhocon import ConfigFactory
from os import path


_mysql = ConfigFactory.parse_file(path.join(path.dirname(__file__), "mysql.conf"))
_redis = ConfigFactory.parse_file(path.join(path.dirname(__file__), "redis.conf"))
_mongodb = ConfigFactory.parse_file(path.join(path.dirname(__file__), "mongodb.conf"))


__all__ = ["_mysql", "_redis", "_mongodb"]