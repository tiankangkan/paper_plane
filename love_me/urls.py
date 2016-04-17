# -*- coding: utf-8 -*-

import views

from django.conf.urls import patterns, url, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^show_form/$', views.reply_to_show_form),
    url(r'paper_plane/$', views.reply_to_paper_plane),
    url(r'paper_plane/do_submit/$', views.reply_to_paper_plane_do_submit)
)
