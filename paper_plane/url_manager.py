# -*- coding: utf-8 -*-

from django.conf import settings


class UrlManager(object):
    host = settings.ENTRY_HOST

    def make_url_with_path(self, path):
        return r'%(host)s%(path)s' % dict(host=self.host, path=path)

    def get_url_of_paper_plane(self):
        path = 'love_me/paper_plane/'
        return self.make_url_with_path(path)

    def get_url_of_weixin_entry(self):
        path = 'subscription/weixin_entry/'
        return self.make_url_with_path(path)