# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OpinionsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field() # 标题
    key_word = scrapy.Field() # 关键词
    url = scrapy.Field() # URL 地址
    content = scrapy.Field() # 内容
    # degist = scrapy.Field() # 摘要
    publish_time = scrapy.Field()   # 发布时间
    source = scrapy.Field()     # 来源
    author = scrapy.Field()     # 作者
    # tenden = scrapy.Field()     # 情感倾向
    media_id = scrapy.Field()   # 媒体类型 ID '0：媒体；1：论坛；2：微博；3：微信；4：博客；5：报刊；6：视频；7：APP
    # level = scrapy.Field()      # 信任分级
    area_id = scrapy.Field()    # data_resource 的 area_id，需要根据另一个表 data_resource 来确认
    comment = scrapy.Field()    # 评论数量
    read = scrapy.Field()       # 阅读数量
    like = scrapy.Field()       # 点赞数量
    transpond = scrapy.Field()  # 转发数
    # digest_id = scrapy.Field()  # 专题 ID
    data_id = scrapy.Field()    # data_resource 的 ID，需要根据另一个表 data_resource 来确认
    create_time = scrapy.Field()    # 创建时间，trigger 更新
    update_time = scrapy.Field()    # 更新时间，trigger 更新
    # tenden_state = scrapy.Field()   # 情感倾向状态 0：待分析；1：分析中；2：已完成
    topic_status = scrapy.Field()   # 话题状态(1置顶，2精选，3热门，4普通，5默认)
