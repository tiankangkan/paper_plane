# -*- coding: utf-8 -*-
# import this file to init django models.

import os, sys
import django
from paper_plane.settings import BASE_DIR

sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'paper_plane.settings'
django.setup()
