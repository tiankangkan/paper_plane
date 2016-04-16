# -*- coding: utf-8 -*-

import views

from django.conf.urls import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^show_form/$', views.reply_to_show_form),
    url(r'paper_plane/$', views.reply_to_paper_plane)
)
