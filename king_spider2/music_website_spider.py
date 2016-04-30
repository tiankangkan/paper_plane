# -*- coding: utf-8 -*-

import scrapy
import datetime
import tzlocal

from items import ArticleItem


class LuoWangSpider(scrapy.Spider):

    name = u'LuoWang'
    start_urls = ['http://www.luoo.net/music/']

    def parse(self, response):
        for href in response.css('.item a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_item)

    def parse_item(self, response):
        item = ArticleItem()
        item.url = response.url
        item.page_type = "music.article"
        item.category = u"落网"
        item.label = ''
        item.label_list = ''
        item.author = ''
        item.title = response.css('.vol-title::text').extract()[0],
        item.cover_url = response.urljoin(response.css('.vol-cover-wrapper img::attr(src)').extract()[0])
        item.desc = response.css('.vol-desc::text').extract()
        item.update_time = datetime.datetime.now(tz=tzlocal.get_localzone())
        yield item
