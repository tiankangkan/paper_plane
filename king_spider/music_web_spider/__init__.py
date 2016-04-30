import os
import sys


def current_file_directory():
    return os.path.dirname(os.path.realpath(__file__))


BASE_DIR = os.path.dirname(os.path.dirname(current_file_directory()))
sys.path.append(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'paper_plane.settings'
