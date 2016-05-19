import json
import re

from k_util.file_op import get_file_list_of_dir

log_dir = '/Users/kangtian/Downloads/logs_2'

file_list = get_file_list_of_dir(log_dir)
file_list.sort()

log_lines = []
for file_path in file_list:
    try:
        with open(file_path, 'rb') as fp:
            log_lines += fp.readlines()
    except:
        print file_path

# print log_lines
' [ID: (?P<id>.*?)]'
re_pattern = r'(?P<time>.*?)MSG_TALKER_TRANSLATE: \[ID: (?P<id>.*?)\] (?P<from>.*?) ->> (?P<from_en>.*?) \|\|->> (?P<to_en>.*?) ->> (?P<to>.*)'

filter_log = []

index = 0
count_dict = {}
for line in log_lines:
    if 'MSG_TALKER_TRANSLATE' in line and ('oA1YQwD6P9e0pB96v_tTvLbSaoUQ' in line or False):
        line = line.decode('string_escape')
        m = re.match(re_pattern, line)
        print line
        if m:
            d = m.groupdict()
            print d
            if 'from' in d and 'to' in d:
                filter_log.append('From: %s (id: %s)\nTo  : %s\n' % (d['from'], d['id'], d['to']))
            if d['id'] in count_dict:
                count_dict[d['id']] += 1
            else:
                count_dict[d['id']] = 1
        index += 1
count_list = [(key, count_dict[key]) for key in count_dict]
count_list.sort(key=lambda i: i[1])
for i in count_list:
    print i
# index = 0
# for line in log_lines:
#     line = line.decode('string_escape')
#     filter_log.append(line)

log_store = '/Users/kangtian/Downloads/logs_2/user_oA1YQwD6P9e0pB96v_tTvLbSaoUQ.log'

with open(log_store, 'w') as fp:
    fp.writelines(filter_log)
