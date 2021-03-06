# -*- coding: utf-8 -*-

import re
import urllib

from django.conf import settings


class UrlManager(object):
    host = settings.ENTRY_HOST

    def make_url_with_path(self, path):
        return r'%(host)s%(path)s' % dict(host=self.host, path=path)

    def get_url_of_paper_plane(self):
        path = 'love_me/paper_plane/'
        return self.make_url_with_path(path)

    def get_url_of_confess(self):
        path = 'love_me/confess/'
        return self.make_url_with_path(path)

    def get_treasure_url(self):
        path = 'treasure/treasure/'
        return self.make_url_with_path(path)

    def get_url_of_weixin_entry(self):
        path = 'subscription/weixin_entry/'
        return self.make_url_with_path(path)

    def get_url_of_res_image(self):
        path = 'common/res_img/'
        return r'%(host)s%(path)s' % dict(host=self.host, path=path)

    def get_url_of_qrcode(self, res_id):
        res_id = str(res_id)
        qrcode_url = '%s%s' % (self.get_url_of_res_image(), res_id)
        return qrcode_url

    def get_warped_url(self, url):
        para = urllib.urlencode(dict(url=url))
        return '/common/agent/?%s' % para

    def url_warp(self, url):
        pattern_douban_img = 'http.*?img.*?\.douban.*?\.com\.*'
        pattern_list = [pattern_douban_img]
        for pattern in pattern_list:
            m = re.match(pattern, url)
            if m:
                url = self.get_warped_url(url)
                break
        url = url.replace('https', 'http')
        return url

url_manager_inst = UrlManager()
