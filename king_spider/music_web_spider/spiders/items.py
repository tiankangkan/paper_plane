# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MusicWebSpiderItem(scrapy.Item):
    page_type = scrapy.Field()
    category = scrapy.Field()
    label = scrapy.Field()
    label_list = scrapy.Field()
    update_time = scrapy.Field()
    page_url = scrapy.Field()
    title = scrapy.Field()
    cover_url = scrapy.Field()
    desc = scrapy.Field()
    author = scrapy.Field()


