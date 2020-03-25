#-*-coding:utf8-*-

import pytest
import os
import sys

sys.path.append("..")

import pymysql

from ScrapyFrame.utils.base import database

class TestClass:
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