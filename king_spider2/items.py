# -*- coding: utf-8 -*-

import scrapy


class ArticleItem(scrapy.Item):
    page_type = scrapy.Field()
    category = scrapy.Field()
    label = scrapy.Field()
    label_list = scrapy.Field()
    update_time = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    cover_url = scrapy.Field()
    desc = scrapy.Field()
    author = scrapy.Field()

