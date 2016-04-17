# -*- coding: utf-8 -*-

import os
from django.conf import settings

from k_util.file_op import make_sure_file_dir_exists
from k_util.time_op import get_time_str_now, TIME_FORMAT_FOR_FILE


class FileManager(object):
    tmp_dir = settings.TEMP_DIR

    def get_tmp_dir(self, *args):
        tmp_dir = os.path.join(self.tmp_dir, *args)
        make_sure_file_dir_exists(tmp_dir, is_dir=True)
        return tmp_dir

    def get_tmp_file(self, *args):
        tmp_file = os.path.join(self.tmp_dir, *args)
        make_sure_file_dir_exists(tmp_file, is_dir=False)
        return tmp_file

    def get_tmp_file_with_stamp(self, *args):
        file_path = self.get_tmp_file(*args)
        time_str = get_time_str_now(TIME_FORMAT_FOR_FILE)
        file_name, ext = os.path.splitext(file_path)
        file_path = '%s__%s%s' % (file_name, time_str, ext)
        make_sure_file_dir_exists(file_path, is_dir=False)
        return file_path

if __name__ == '__main__':
    fm = FileManager()
    print fm.get_tmp_file_with_stamp('as', 'voice', 'f.txt')