# -*- coding: utf-8 -*-

import scrapy
import datetime
import tzlocal
import time

from k_util.time_op import get_time_str_unique, TZ_LOCAL, convert_time_obj_to_time_str, TIME_FORMAT_FOR_FILE
from items import MusicWebSpiderItem
from music_rss.models import PageType


def get_first_item_of_list(obj):
    while True:
        if isinstance(obj, list) and obj:
            obj = obj[0]
        else:
            break
    return obj


def flat_item_of_list(obj):
    result_list = list()
    if isinstance(obj, list) and not isinstance(obj, basestring) and len(obj) > 0:
        for item in obj:
            result_list += flat_item_of_list(item)
    else:
        result_list = [obj]
    return result_list


def get_text_of_list(obj):
    return clean_string('\n'.join(flat_item_of_list(obj)))


def clean_string(s):
    s = ''.join([' ' if c.isspace() else c for c in s])
    s = ' '.join(s.split(' '))
    s = '\n'.join(s.split('\n'))
    return s


class StackOverflowSpider(scrapy.Spider):
    name = 'stackoverflow'
    start_urls = ['http://stackoverflow.com/questions?sort=votes']

    def parse(self, response):
        for href in response.css('.question-summary h3 a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_question)

    def parse_question(self, response):
        yield {
            'title': response.css('h1 a::text').extract()[0],
            'votes': response.css('.question .vote-count-post::text').extract()[0],
            'body': response.css('.question .post-text').extract()[0],
            'tags': response.css('.question .post-tag::text').extract(),
            'link': response.url,
        }


class LuoWangJournalSpider(scrapy.Spider):
    name = 'LuoWangJournal'
    start_urls = ['http://www.luoo.net/music/']

    def parse(self, response):
        for href in response.css('.item a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_item)

    def parse_item(self, response):
        item = MusicWebSpiderItem()
        item['page_url'] = response.url
        item['page_type'] = PageType.MUSIC_ARTICLE
        item['category'] = u"落网"
        item['label'] = ''
        item['label_list'] = ''
        item['author'] = ''
        item['title'] = get_text_of_list(response.css('.vol-title::text').extract()[0])
        item['cover_url'] = response.urljoin(response.css('.vol-cover-wrapper img::attr(src)').extract()[0])
        item['desc'] = get_text_of_list(response.css('.vol-desc::text').extract())
        t = datetime.datetime.now(tz=TZ_LOCAL)
        item['update_time'] = t
        item['update_time_str'] = get_time_str_unique(time_obj=t, time_format=TIME_FORMAT_FOR_FILE)
        yield item


class LuoWangEssaysSpider(scrapy.Spider):
    name = 'LuoWangEssays'
    start_urls = ['http://www.luoo.net/essays/']

    def parse(self, response):
        href_list = list()
        href = get_first_item_of_list(response.css('.essay-banner .meta a::attr(href)').extract()[0])
        href_old_list = flat_item_of_list(response.css('.essay-list div a::attr(href)').extract())
        href_list.append(href)
        href_list += href_old_list
        print 'url_list: ', href_list
        for href in set(href_list):
            full_url = response.urljoin(href)
            yield scrapy.Request(full_url, callback=self.parse_essays)

    def parse_essays(self, response):
        item = MusicWebSpiderItem()
        item['page_url'] = response.url
        item['page_type'] = PageType.MUSIC_ARTICLE
        item['category'] = u"落网"
        item['label'] = ''
        item['label_list'] = ''
        item['author'] = ''
        item['title'] = get_text_of_list(response.css('.essay-title ::text').extract()[0])
        item['cover_url'] = response.urljoin(response.css('.essay-content img::attr(src)').extract()[0])
        item['desc'] = get_text_of_list(response.css('.essay-content ::text').extract())[:225]
        t = datetime.datetime.now(tz=TZ_LOCAL)
        item['update_time'] = t
        item['update_time_str'] = get_time_str_unique(convert_time_obj_to_time_str(t, TIME_FORMAT_FOR_FILE))
        yield item

if __name__ == "__main__":
    pass

