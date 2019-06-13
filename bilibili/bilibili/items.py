# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class VideoItem(scrapy.Item):
    title = scrapy.Field()
    coverUrl = scrapy.Field()
    videoUrl = scrapy.Field()
    videoDownUrl = scrapy.Field()
    createTime = scrapy.Field()
    author = scrapy.Field()
