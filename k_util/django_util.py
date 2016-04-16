# -*- coding: UTF-8 -*-

"""
Desc: django util.
Note:

---------------------------------------
# 2016/04/17   kangtian         created

"""


def get_request_body(request, raw=None):
    """
    :param request:
    :param raw: raw = 'GET' | 'POST'
    :return:
    """

    body_dict = dict()
    if 'GET' == raw or 'POST' == raw:
        d = getattr(request, raw)
        if d:
            body_dict.update(d)
    else:
        if request.GET:
            body_dict.update(request.GET)
        if request.POST:
            body_dict.update(request.POST)
        if request.REQUEST:
            body_dict.update(request.REQUEST)
    return body_dict

