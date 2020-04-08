[toc]

# 1. Description

解决多人爬虫协作，管理不方便的问题。先搭建需要的基本 Scrapy 框架，并且明确命名规范。

# 2. Requirements

* Python >= 3.7
* scrapy >= 2.0
* pymysql = 0.9.3
* pymongo=3.10.1

## 2.1 Configuration

配置采用 `HOCON` 解析数据库相关配置数据——python 版本的支持 package 为 [`pyhocon`](https://github.com/chimpler/pyhocon/)。配置文件结构为：

```bash
.
├── ScrapyFrame
│   └── utils
│       ├── base
│       │   └── database.py
│       └── conf
│           ├── __init__.py
│           ├── mysql.conf # mysql 基本配置文件
│           ├── redis.conf # redis 基本配置文件
│           └── mongodb.conf # mongo 基本配置文件
```

### 2.1.1 MySQL Connect

`MySQL` 连接已经在 `base` 的 `database.py` 脚本中完成了基本连接操作，可以直接使用一个 database 连接，也可以后期使用 cursor 属性赋值方式完成：

```python
from ScrapyFrame.utils.base.database import *
conn = MySQLConnect() # 需要直接连接一个 Database 可以传入 database 的名称 eg: conn = MySQLConnect("hzjy_test")
# 获取 connection 属性，和 pymysql.connections.Connection 对象相同
conn.connection

# 创建 cursor，根据是否已经连接数据库返回不同的数据
conn.cursor

# 更改数据库或者首次连接数据库
conn.cursor = "hzjy_test"

# 执行查询命令
conn.cursor.execute("SHOW TABLES;") 
```

### 2.1.2 Redis Connect

`Redis` 连接的基本配置在 `conf`  文件夹的 `redis.conf` 文件中，该对象是继承了 `redis.StrictRedis` ，除了定制的 `Connection` 属性和 `ping` 方法外，可以直接使用 `redis` 的方法：

```python
from ScrapyFrame.utils.base.database import *
conn = RedisConnect() 

# 连接对象
conn.Connection 

# 检查数据是否为列表成员
conn.sismember("DataItem", '124987')
```

### 2.1.3 MongoDB Connect

`MongoDB` 基本配置文件在 `conf` 文件夹的 `mongodb.conf` 文件中，连接对象是继承了 `pymongo.MongoClient`，拥有 `database` 、`connection` 属性，定制化了 `drop_database` 方法。需要使用 MongoDB 中的 collections 可以直接使用 `database` 属性创建，其他方法和属性直接继承 `pymongo.MongoClient` ：

```python
import datatime
from ScrapyFrame.utils.base.database import *

# 可以直接连接 databse，需要注意⚠️必须使用 keywrod 形式传入 conn = MongoDBConnect(db="test")
conn = MongoDBConnect() 

# 连接对象
conn = conn.Connection

# 连接的数据库
conn.database

# 更改或者设置连接的数据库
conn.database = "test"

# 插入数据到 student collection：
#		1. 创建 collection 对象
#		2. 写入数据
student = conn.database.student

post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

# 插入数据与查询 ID
post_id = student.insert_one(post).inserted_id

post_id
```

## 2.2 Middleware & Pipeline & Filter

### 2.2.1 RandomUserAgentDownloaderMiddleware

随机化 UserAgent Middleware 类，启用是参考一般的 Middleware 方式—— `ScrapyFrame.middlewares.RandomUserAgentDownloaderMiddleware`。默认已经配置了可选择的 User-Agent，可以通过在 `settings` 添加比较的 `UserAgent` 序列。

### 2.2.2 RandomDelayDownloaderMiddleware

随机化延迟请求 middleware 类，启用方式在 `DOWNLOADER_MIDDLEWARES` 调用: `ScrapyFrame.middlewares.RandomDelayDownloaderMiddleware`。可以配置最大延迟时间（秒数），需要在 `settings` 中配置 `RANDOM_DELAY`

### 2.2.3 CustomizeRFPDupeFilter

定制化的重复请求筛选，该请求是主要是通过 `Cache database` 的方式进行筛选，目前定义的是使用 `redis` 来完成，启用方式分分为多个类型：

```python
# 启用该筛选类
DUPEFILTER_CLASS =’ScrapyFrame.dupefilters.CustomizeRFPDupeFilter'
# 启用筛选调试日志
DUPEFILTER_DEBUG=True
# 明确 cache database 名称，由 SPIDER_NAME 确认
SPIDER_NAME

### 以上内容需要在 settings 中进行配置，用于检测 unique 的数据需要在 reqeust 的 meta 中传入
request.meta.get("UNIQUE_ID")
```

目前明确的筛选方式，是需要通过 `UNIQUE_ID` 来确认是否已经爬取过。



# 3. Run

进入 `ScrapyFrame` 项目文件夹中，启动相关爬虫：

1. 检查已有爬虫——`scrapy list`
2. 启动相关爬虫——`scrapy crawl <spider-name>`

