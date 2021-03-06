# -*- coding: utf-8 -*-

import views
import os

from django.conf.urls import patterns, url, include
from django.contrib import admin
from paper_plane.file_manager import FileManager

admin.autodiscover()

qrcode_dir = os.path.dirname(FileManager().get_path_of_qrcode('any'))
# qrcode_dir = '/data/res/img/qrcode'

urlpatterns = patterns('django.views.static',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^res_img/(?P<path>.*)$', 'serve', {'document_root': qrcode_dir}),
    url(r'^agent/$', views.reply_to_agent),
)
