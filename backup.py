# crontab: 0 0 * * * python "/data/project/paper_plane/backup.py"
# my-mac-crontab: 0 0 * * * python "/Users/kangtian/Documents/Master/paper_plane/backup.py"

from k_util.backup import FileBackup, FILTER_ONE_DAY

dir_config_list = [
    dict(dir_path='/data/logs/custom/', filter_func=FILTER_ONE_DAY),
    dict(dir_path='/data/logs/error/', filter_func=FILTER_ONE_DAY),
]

dir_config_list_test = [
    dict(dir_path='/Users/kangtian/Documents/Master/paper_plane', filter_func=FILTER_ONE_DAY),
]


if __name__ == '__main__':
    f = FileBackup(dir_config_list=dir_config_list, to_dir='/tmp/log_backup/')
    f.back_up()
    print 'Backup OK ~'
