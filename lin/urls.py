# -*- coding: utf-8 -*-

import views

from django.conf.urls import patterns, url, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^do_you_love_me/$', views.reply_to_do_you_love_me),
    url(r'^you_are_the_one/$', views.reply_to_you_are_the_one),
)
