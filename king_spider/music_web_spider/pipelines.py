# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import copy

from k_util.hash_util import gen_md5
from spiders.items import MusicWebSpiderItemJEncoder
from music_rss.models import WebPageInfo, PageType


class MusicWebSpiderPipeline(object):
    def process_item(self, item, spider):
        i = item
        if i['page_type'] == PageType.MUSIC_ARTICLE:
            i_static = copy.deepcopy(i)
            i_static.pop('update_time')
            i_static.pop('update_time_str')
            i_static_json = json.dumps(dict(i_static), cls=MusicWebSpiderItemJEncoder)
            identify = str(gen_md5(i_static_json))
            content = json.dumps(dict(i), cls=MusicWebSpiderItemJEncoder)
            if not len(WebPageInfo.objects.filter(identify=identify)):
                web_page_info = WebPageInfo(
                    page_type=i['page_type'],
                    category=i['category'],
                    label=i['label'],
                    label_list=i['label_list'],
                    update_time=i['update_time'],
                    update_time_str=i['update_time_str'],
                    page_url=i['page_url'],
                    title=i['title'],
                    content=content,
                    identify=identify
                )
                web_page_info.save()
        return item
