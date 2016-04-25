import json
import re

from k_util.file_op import get_file_list_of_dir

log_dir = '/Users/kangtian/Downloads/logs'

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
for line in log_lines:
    if 'MSG_TALKER_TRANSLATE' in line and 'oA1YQwISCJZY0b8RTswvdKOZWzQA' in line:
        line = line.decode('string_escape')
        m = re.match(re_pattern, line)
        print line
        if m:
            d = m.groupdict()
            print d
            if 'from' in d and 'to' in d:
                if index % 2 == 0:
                    filter_log.append('From: %s\nTo  : %s\n' % (d['from'], d['to']))
        index += 1

# index = 0
# for line in log_lines:
#     line = line.decode('string_escape')
#     filter_log.append(line)

log_store = '/Users/kangtian/Downloads/logs/all_in_one_lin.log'

with open(log_store, 'w') as fp:
    fp.writelines(filter_log)
