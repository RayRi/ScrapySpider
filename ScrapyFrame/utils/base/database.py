#-*-coding:utf8-*-
"""
Descriptions:
    The script is about Connection class, like connect mysql or redis
    * MySQLConnect, connect mysql database with basic configuration, there is not
        database specified
"""

from __future__ import absolute_import

import pymysql
import redis
import pymongo
import logging

from ScrapyFrame.utils.conf import *

class DBConnector(object):
    @property
    def _logger(self):
        """Logger Property"""
        logger = logging.getLogger(self.__class__.__name__)
        return logging.LoggerAdapter(logger, {"Database": self})
        

    def log(self, message, level=logging.DEBUG, **kwargs):
        """Run logger to display log information"""
        self._logger.log(level, message, **kwargs)
    
    def close(self):
        """Close Connection"""
        if hasattr(self, "connection"):
            self.connection.close()
        elif hasattr(self, "Connection"):
            self.Connection.close()


class MySQLConnect(DBConnector):
    """MySQL Connection Obejct

    Connect the MySQL database with basic configuration, which there is not database
    connected in default configuration. But database can be specified with assign
    a database to property cursor.

    Properties:
        Connection: connect RDBM with default mysql config
        connection: pymysql.connections.Connection object, same with Connection
        cursor: pymyql.cursors object. If object with a db at initialize, there 
            is the object. Otherwise, get a cursor object with assigning a db
        _cursor: a method create a pymysql.cursors
        connect: a method create pymysql.connections.Connection object
    Arguments:
        db: a database name that is used to select database, default None don't 
            use any database

    Examples:
        >>> from ScrapyFrame.utils.base.database import *
        >>> conn = MySQLConnect()
        >>> conn.connection
            <pymysql.connections.Connection at 0x10afcec50>
        >>> conn.cursor
            "Database isn't connected"
        >>> conn.cursor = "hzjy_test"
        >>> conn.cursor
            <pymysql.cursors.Cursor at 0x10a461750>
        >>> conn.cursor.execute("SHOW TABLES;") 
    """


    def __init__(self, db=None):
        self.Connection = self.connect()

        if db is not None:
            self.Connection.select_db(db)
            self.Connection.db = db


    def connect(self):
        return pymysql.connect(**_mysql)


    @property
    def connection(self):
        return self.Connection


    @property
    def cursor(self):
        return self.Connection.cursor()
    

    @cursor.setter
    def cursor(self, db):
        return self._cursor(db)

    
    @cursor.getter
    def cursor(self):
        if self.Connection.db is None:
            return "Database isn't connected"
        else:
            self.log(f"Database {self.Connection.db} is connected", level=logging.INFO)
            return self.Connection.cursor() 


    def _cursor(self, db):
        # connect a new database
        if not self.Connection.db:
            self.Connection.select_db(db)
            self.Connection.db = db
        else:
            logging.info(f"Convert database {self.Connection.db} to {db}")
            self.Connection.select_db(db)
            self.Connection.db = db
        
        return self.Connection.cursor()



class RedisConnect(redis.StrictRedis, DBConnector):
    """Redis Connection Obejct

    Connect the redis database with configuration, and there is not database
    connected in default configuration. The connection method is a connection pool.
    Besides, it's inherient from redis.StrictRedis. Another methods can be used
    like common redis object

    Properties:
        Connection: it's a alternative RedisConnect object 
        ping: a method check connection status

    Examples:
        >>> from ScrapyFrame.utils.base.database import *
        >>> conn = RedisConnect()
        >>> conn.Connection
            ScrapyFrame.utils.base.database.RedisConnect
        >>> conn.__class__.__base__
            redis.client.Redis
        >>> conn.cursor.keys("*")
            DataItem
        >>> conn.sismember("DataItem", '124987')
            False
    """
    def __init__(self,  **kwargs):
        connection_pool = redis.ConnectionPool(**_redis)
        _redis.update(kwargs)
        super().__init__(connection_pool=connection_pool, **_redis)


    def ping(self):
        if not super().ping():
            super(DBConnector, self).log("Can't connect redis server", level=logging.ERROR)
        return super().ping()
            
    @property
    def Connection(self):
        return self


class MongoDBConnect(pymongo.MongoClient, DBConnector):
    """MongoDB Connection Object

    Connect mongodb client
    """
    def __init__(self, *, db=None, **kwargs):
        super().__init__(**_mongodb, **kwargs)

        # Initialize the database, if db is not None
        if db not in self.list_database_names():
            if db is not None:
                self.log(f"Initialize database {db}", level=logging.INFO)
                self._db = self[db]
            else:
                self._db = None
        else:
            self._db = self[db]


    @property
    def Connection(self):
        return self


    @property
    def database(self):
        if self._db is None:
            self.log(f"Database is not created", level=logging.DEBUG)
        return self._db
        

    @database.setter
    def database(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Database name must be string, but get {type(value)}")
        
        if value not in self.list_database_names():
            self.log(f"Change database {self.database._Database__name} to {value}")
        self._db = self[value]

    
    @database.getter
    def database(self):
        return self._db

    
    @database.deleter
    def database(self):
        self._db = None

    
    def drop_database(self, db, **kwargs):
        """Drop Database"""
        super().drop_database(db, **kwargs)
        self._db = None
