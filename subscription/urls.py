# -*- coding: utf-8 -*-

import views

from django.conf.urls import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^weixin_entry/$', views.weixin_entry),
)
