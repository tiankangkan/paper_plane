# -*- coding: UTF-8 -*-

"""
Desc: talker setting.
Note:

---------------------------------------
# 2016/04/07   lin              created

"""

import os
import platform


BASE_DIR = os.path.dirname(__file__)
SYSTEM = platform.system().lower()

TEMP_DIR = '/tmp/temp_talker/'
if 'windows' in SYSTEM:
    TEMP_DIR = 'D:\\temp_talker\\'
else:
    TEMP_DIR = '/tmp/temp_talker/'

