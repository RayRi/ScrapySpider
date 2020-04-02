#-*-coding:utf8-*-

import pytest
import os
import sys

sys.path.append("..")

import pymysql
import redis
import pymongo

from ScrapyFrame.utils.base import database

class TestMySQLClass:
    def test_initial(self):
        conn1 = database.MySQLConnect()
        conn2 = database.MySQLConnect("hzjy_test")
        self.conn1 = conn1
        self.conn2 = conn2

        assert type(conn1.Connection) == pymysql.connections.Connection
        assert type(conn1.connection) == pymysql.connections.Connection
        assert type(conn2.Connection) == pymysql.connections.Connection
        assert type(conn2.connection) == pymysql.connections.Connection


    def test_cursor(self):
        conn1 = database.MySQLConnect()
        conn2 = database.MySQLConnect("hzjy_test")
        assert conn1.cursor == "Database isn't connected"
        assert type(conn2.cursor) == pymysql.cursors.Cursor
        
    
    def test_db(self):
        conn1 = database.MySQLConnect()
        conn2 = database.MySQLConnect("hzjy_test")
        assert conn1.connection.db is None
        assert conn2.connection.db == "hzjy_test"

class TestRedisClass:
    def test_initial(self):
        conn = database.RedisConnect()
        assert conn.__class__.__base__  == redis.client.Redis
        assert conn.Connection.__class__.__base__  == redis.client.Redis


    def test_ping(self):
        conn = database.RedisConnect()
        assert isinstance(conn.ping(), bool)

    
    def test_db(self):
        conn = database.RedisConnect()
        assert "DoubanDataItem" in conn.keys("*")


class TestMongoDB:
    def test_initial(self):
        conn = database.MongoDBConnect()
        assert conn.__class__.__base__ == pymongo.mongo_client.MongoClient
        assert conn.connection.__class__.__base__ == pymongo.mongo_client.MongoClient


    def test_database(self):
        conn = database.MongoDBConnect()
        conn1 = database.MongoDBConnect(db="test")
        assert isinstance(conn1.database, pymongo.database.Database)
        assert conn1.database._Database__name == "test", "Database name is not correct"
        
        conn.database = "test"
        assert conn.database._Database__name == "test", "Database name is not correct"