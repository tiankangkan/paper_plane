# -*- coding: utf-8 -*-

import os
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import love_me.urls
import lin.urls
import subscription.urls
import common.urls
import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^love_me/', include(love_me.urls)),
    url(r'^lin/', include(lin.urls)),
    url(r'^subscription/', include(subscription.urls)),
    url(r'^common/', include(common.urls)),
)

urlpatterns += patterns('django.views.static',
    url(r'^static/(?P<path>.*)$', 'serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^jslib/(?P<path>.*)$', 'serve', {'document_root': os.path.join(settings.STATIC_ROOT, 'jslib')}),
    url(r'^css/(?P<path>.*)$', 'serve', {'document_root': os.path.join(settings.TEMPLATE_ROOT, 'css')}),
    url(r'^media/(?P<path>.*)$', 'serve', {'document_root': os.path.join(settings.STATIC_ROOT, 'media')}),
)