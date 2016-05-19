import sys
import os

def current_file_directory():
    return os.path.dirname(os.path.realpath(__file__))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(BASE_DIR)

from paper_plane import django_models_init

from treasure.models import FileMapping, TREASURE_FILE_MUN
from k_util.hash_util import gen_md5

BT_DIR = '/data/res/bt'


def insert_bt_info_to_db():
    for root, dirs, file_names in os.walk(BT_DIR):
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            identify = gen_md5(file_path)
            file_new_path = os.path.join(root, '%s.torrent' % identify)
            os.rename(file_path, file_new_path)
            print 'old_path: %s' % file_path
            print 'new_path: %s' % file_new_path
            f_item = FileMapping(identify=identify, file_path=file_new_path)
            f_item.save()


if __name__ == '__main__':
    # insert_bt_info_to_db()
    print TREASURE_FILE_MUN
