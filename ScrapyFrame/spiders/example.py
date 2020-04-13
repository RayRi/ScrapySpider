# -*- coding: utf-8 -*-
import scrapy
import json
import re
import time
import logging

from os import path

from ScrapyFrame.items import OpinionsItem
# 定制化 Spider，继承自 scrapy.Spider
from ScrapyFrame.utils import base

class BasicToutiaoSpider(base.SpiderBase):
    name = 'news'
    _logger = logging.getLogger(__name__+"."+name)
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        # "FEED_EXPORT_ENCODING" :'utf-8',
        "CONCURRENT_REQUESTS":2,
        "REFERRER_POLICY": "no-referrer-when-downgrade",
        # 去重处理
        "DUPEFILTER_CLASS":'ScrapyFrame.dupefilters.CustomizeRFPDupeFilter',
        "SPIDER_NAME":name,
        # "DUPEFILTER_DEBUG": False,
        # 默认 HEADERS
        "DEFAULT_REQUEST_HEADERS":{
            "Accept": "*/*",
            # "Content-Type": "text/html; charset=gbk",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Connection": "keep-alive",
            "Host": "temp.163.com",
            "Referer": "https://news.163.com/domestic/",
            "Sec-Fetch-Dest": "script",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        },
        # 需要写入数据的字段
        "OPINION_FIELDS":[
            "title","key_word","url","content","degist","publish_time","source","author",
            "tenden","media_id","level","area_id","comment","read","like","transpond",
            "digest_id","data_id","tenden_state","topic_status"
        ],
        # middlewares
        "DOWNLOADER_MIDDLEWARES": {
            'ScrapyFrame.middlewares.RandomUserAgentDownloaderMiddleware': 10,
        },
        # pipelines
        "ITEM_PIPELINES": {
            'ScrapyFrame.pipelines.MongoDBPipeline': 500,
            'ScrapyFrame.pipelines.MySQLPipeline': 700,

        },
        # database settings
        "db": "opinion_test",
        "default_tb": "tbl_opinion", 
        "db_cache": "redis",
        # Logs
        "LOG_ENABLED": False,
        "LOG_ENCODING": "utf8",
        # "LOG_LEVEL": "INFO",
        "LOG_FILE": path.join(path.dirname(__file__), \
            "../../Logs/{name}_{date}.log".format(name=name, date=time.strftime("%Y%m%d", time.localtime())))
    }

    allowed_domains = ['163.com']
    _start_url = 'https://temp.163.com/special/00804KVA/cm_guonei{0}.js?callback=data_callback'

    def start_requests(self):
        for i in ['', '_02', '_03']:
            url = self._start_url.format(i)
            self.log(f"Initial url: {url}")
            yield scrapy.Request(url, callback=self.parse, \
                meta={"source": "NetEasy"})
            # break
    


    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        # 网易新闻需要转码为 gbk
        self.log(f"URL: {response.url} Response Correct")
        text = response.body.decode("gbk").replace("data_callback(", "")[:-1]
        data = json.loads(text)

        # 需要通过 meta 传递必要的数据
        for element in data:
            url = element.get("docurl", "")
            if not url:
                continue

            information = {}
            information["title"] = element.get("title", "")
            information["url"] = url
            information["key_word"] = [item.get("keyname") for item in element.get("keywords", {}) if item.get("keyname", False)]
            if element.get("time", False):
                information["publish_time"] = time.strftime("%Y-%m-%d %H:%M:%S", \
                    time.strptime(element.get("time", ""), "%m/%d/%Y %H:%M:%S"))
            else:
                information["publish_time"] = None
            information["author"] = element.get("source", "")

            # 文章的 URL 中可以解析出独特的信息作为 UNIQUE_ID, eg: 'https://news.163.com/20/0408/20/F9NI94JR0001899O.html'
            unique_id = url.split("/")[-1].replace(r".html", "")

            
            yield scrapy.Request(url, callback=self.parse_item, \
                meta={"information": information, "UNIQUE_ID": unique_id})





    def parse_item(self, response):

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        item = OpinionsItem()
        self.log(f"{response.url} Response Correct", level=logging.DEBUG)

        # 更新数据
        item.update(response.meta.get("information"))
        pattern = re.compile('<script.*? type="text/javascript">.*?</script>', re.S|re.M)
        content = pattern.sub("", response.css("div.post_text ").extract_first())
        item["content"] = content
        item["source"] = u"网易新闻"
    
        item["media_id"] = "13"
        item["area_id"] = "12"
        item["comment"] = 0
        item["read"] = 0
        item["like"] = 0
        item["transpond"] = 0
        item["data_id"] = "78"
        item["topic_status"] = "4"

        yield item