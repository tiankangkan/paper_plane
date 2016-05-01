# -*- coding: utf-8 -*-


def get_first_item_of_list(obj):
    while True:
        if isinstance(obj, list) and obj:
            obj = obj[0]
        else:
            break
    return obj


def flat_item_of_list(obj):
    result_list = list()
    if isinstance(obj, list) and not isinstance(obj, basestring) and len(obj) > 0:
        for item in obj:
            result_list += flat_item_of_list(item)
    else:
        result_list = [obj]
    return result_list


def get_text_of_list(obj):
    return clean_string('\n'.join(flat_item_of_list(obj)))


def clean_string(s):
    s = ''.join([' ' if c.isspace() else c for c in s])
    s = ' '.join(s.split(' '))
    s = '\n'.join(s.split('\n'))
    return s
