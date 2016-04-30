# -*- coding: utf-8 -*-

import scrapy
import datetime
import tzlocal

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
    return '\n'.join(flat_item_of_list(obj))


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


class LuoWangSpider(scrapy.Spider):
    name = 'LuoWang'
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
        item['update_time'] = datetime.datetime.now(tz=tzlocal.get_localzone())
        yield item

#
# if __name__ == "__main__":
#     print get_text_of_list(["我的", ['hello', ['haha', 'wode'], 'world']])
#
