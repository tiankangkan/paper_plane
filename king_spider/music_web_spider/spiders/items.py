# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import json

from k_util.time_op import get_time_str_unique, TZ_LOCAL, convert_time_obj_to_time_str, TIME_FORMAT_FOR_FILE


class MusicWebSpiderItem(scrapy.Item):
    page_type = scrapy.Field()
    category = scrapy.Field()
    update_time = scrapy.Field()
    update_time_str = scrapy.Field()
    page_url = scrapy.Field()
    title = scrapy.Field()
    cover_url = scrapy.Field()
    desc = scrapy.Field()
    author = scrapy.Field()
    label = scrapy.Field()
    label_list = scrapy.Field()

    def set_values(self, page_type, category, update_time=None, update_time_str=None, page_url=None, title=None,
                   cover_url=None, desc=None, author=None, label=None, label_list=None):
        if not update_time or not update_time_str:
            t = datetime.datetime.now(tz=TZ_LOCAL)
            update_time = t
            update_time_str = get_time_str_unique(convert_time_obj_to_time_str(t, TIME_FORMAT_FOR_FILE))
        self['page_type'] = page_type
        self['category'] = category
        self['update_time'] = update_time
        self['update_time_str'] = update_time_str
        self['page_url'] = page_url or ''
        self['title'] = title or ''
        self['cover_url'] = cover_url or ''
        self['desc'] = desc or ''
        self['author'] = author or ''
        self['label'] = label or ''
        self['label_list'] = label_list or ''


class MusicWebSpiderItemJEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return convert_time_obj_to_time_str(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)




