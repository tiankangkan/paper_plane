# -*- coding: utf-8 -*-

import views

from django.conf.urls import patterns, url, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'one_page/$', views.reply_to_one_page),
    url(r'one_page/get_more/$', views.reply_to_one_page_get_more),
)
