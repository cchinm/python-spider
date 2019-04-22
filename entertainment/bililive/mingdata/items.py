# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MingdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BiliItem(scrapy.Item):

    tid = scrapy.Field()
    pid = scrapy.Field()
    ctime = scrapy.Field()
    male = scrapy.Field()
    count = scrapy.Field()
    total = scrapy.Field()
    female = scrapy.Field()
    max_count = scrapy.Field()
    room_id = scrapy.Field()