# -*- coding: utf-8 -*-

import views
import os

from django.conf.urls import patterns, url, include
from django.contrib import admin
from paper_plane.file_manager import FileManager

admin.autodiscover()

treasure_dir = os.path.dirname(FileManager().get_path_of_treasure('any'))
# qrcode_dir = '/data/res/img/qrcode'

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^treasure/$', views.reply_to_treasure),
    url(r'^treasure/get_url/$', views.reply_to_treasure_get_url),
)

urlpatterns += patterns('django.views.static',
    url(r'^res_treasure/(?P<path>.*)$', 'serve', {'document_root': treasure_dir}),
)
