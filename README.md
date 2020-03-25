[toc]

# 1. Description

解决多人爬虫协作，管理不方便的问题。先搭建需要的基本 Scrapy 框架，并且明确命名规范。

# 2. Requirements

* Python >= 3.7
* scrapy >= 2.0
* pymysql = 0.9.3

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
│           └── redis.conf # redis 基本配置文件
```

### 2.1.1 MySQL Connect

`MySQL` 连接已经在 `base` 的 `database.py` 脚本中完成了基本连接操作，可以直接使用一个 database 连接，也可以后期使用 cursor 属性赋值方式完成：

```python
from ScrapyFrame.utils.base.database import *
conn = MySQLConnect()
# 获取 connection 属性，和 pymysql.connections.Connection 相同
conn.connection

# 创建 cursor，根据是否已经连接数据库返回不同的数据
conn.cursor

# 更改数据库或者首次连接数据库
conn.cursor = "hzjy_test"

# 执行查询命令
conn.cursor.execute("SHOW TABLES;") 
```



# 3. Run

进入 `ScrapyFrame` 项目文件夹中，启动相关爬虫：

1. 检查已有爬虫——`scrapy list`
2. 启动相关爬虫——`scrapy crawl <spider-name>`

