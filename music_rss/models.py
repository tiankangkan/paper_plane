# -*- coding: utf-8 -*-

from django.db import models


class PageType(object):
    MUSIC_ARTICLE = 'MUSIC_ARTICLE'
    MUSIC_FM = 'MUSIC_FM'


class CategoryType(object):
    WEB_LUO_WANG = 'WEB_LUO_WANG'
    WEB_MAI_TIAN = 'WEB_MAI_TIAN'
    WEB_YI_KE = 'WEB_YI_KE'


class WebPageInfo(models.Model):
    identify = models.CharField(primary_key=True, db_index=True, max_length=64)    # maybe md5 of content ?
    page_type = models.CharField(db_index=True, blank=True, null=True, max_length=64)
    category = models.CharField(db_index=True, blank=True, null=True, max_length=64)
    label = models.CharField(db_index=True, blank=True, null=True, max_length=64)
    label_list = models.CharField(db_index=True, blank=True, null=True, max_length=256)
    update_time = models.DateTimeField(db_index=True, blank=True, null=True)
    update_time_str = models.CharField(db_index=True, blank=True, null=True, max_length=64)
    page_url = models.TextField(blank=True, null=True)
    title = models.CharField(db_index=True, blank=True, null=True, max_length=1024)
    content = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'web_page_info'

    def __str__(self):
        return 'update_time: %s, type: %s, category:%s, label: %s, page_url: %s' % (self.update_time, self.page_type, self.category, self.label, self.page_url)
