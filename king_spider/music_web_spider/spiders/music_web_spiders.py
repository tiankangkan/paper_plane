# -*- coding: utf-8 -*-

import scrapy
import json

from items import MusicWebSpiderItem, MusicWebSpiderItemJEncoder
from music_rss.models import PageType, CategoryType
from spider_util import get_first_item_of_list, flat_item_of_list, get_text_of_list, clean_string


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
        item.set_values(
            page_url=response.url,
            page_type=PageType.MUSIC_ARTICLE,
            category=CategoryType.WEB_LUO_WANG,
            title=get_text_of_list(response.css('.vol-title::text').extract()[0]),
            cover_url=response.urljoin(response.css('.vol-cover-wrapper img::attr(src)').extract()[0]),
            desc=get_text_of_list(response.css('.vol-desc::text').extract())
        )
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
        for href in set(href_list):
            full_url = response.urljoin(href)
            yield scrapy.Request(full_url, callback=self.parse_essays)

    def parse_essays(self, response):
        item = MusicWebSpiderItem()
        item.set_values(
            page_url=response.url,
            page_type=PageType.MUSIC_ARTICLE,
            category=CategoryType.WEB_LUO_WANG,
            title=get_text_of_list(response.css('.essay-title ::text').extract()[0]),
            cover_url=response.urljoin(response.css('.essay-content img::attr(src)').extract()[0]),
            desc=get_text_of_list(response.css('.essay-content ::text').extract())[:225]
        )
        yield item


class DouBanYiKeSpider(scrapy.Spider):
    name = 'YiKeEssays'
    start_urls = ['http://www.doubanyike.com/mapi.php?fun=stream&columnId=52&page=1']    # 52 是[听音乐].

    def parse(self, response):
        article_list = json.loads(response.body)
        print json.dumps(article_list, indent=4)
        # import time
        # time.sleep(1000)
        for article in article_list:
            item = MusicWebSpiderItem()
            thumbs = json.loads(article['thumbs'])
            cover_url = response.urljoin(thumbs[0]['large']['url'])
            item.set_values(
                page_url=article['url'],
                page_type=PageType.MUSIC_ARTICLE,
                category=CategoryType.WEB_YI_KE,
                title=article['title'],
                cover_url=cover_url,
                desc=article['abstract']
            )
            yield item


if __name__ == "__main__":
    pass

