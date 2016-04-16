# -*- coding: utf-8 -*-

import views

from django.conf.urls import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^token/$', views.reply_to_token),
)
