# -*- coding: utf-8 -*-
# import this file to init django models.

import os, sys
import django


def current_file_directory():
    return os.path.dirname(os.path.realpath(__file__))


BASE_DIR = os.path.dirname(current_file_directory())
sys.path.append(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'paper_plane.settings'
django.setup()
