# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

from k_util.hash_util import gen_md5
from music_rss.models import WebPageInfo, PageType


class MusicWebSpiderPipeline(object):
    def process_item(self, item, spider):
        i = item
        if i['page_type'] == PageType.MUSIC_ARTICLE:
            update_time = i['update_time']
            i.pop('update_time')
            content = json.dumps(dict(i))    # update time make identify be wrong.
            identify = str(gen_md5(content))
            web_page_info = WebPageInfo(
                page_type=i['page_type'],
                category=i['page_type'],
                label=i['label'],
                label_list=i['label_list'],
                update_time=update_time,
                page_url=i['page_url'],
                title=i['title'],
                content=content,
                identify=identify
            )
            web_page_info.save()
        return ''
