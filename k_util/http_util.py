# -*- coding: UTF-8 -*-

"""
Desc: django util.
Note:

---------------------------------------
# 2016/04/17   kangtian         created

"""
import json
import urllib, urllib2


def post_request(url, values=None, method='POST'):
    values = values or dict()
    if method == 'POST':
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data=data)
    else:
        req = urllib2.Request(url, headers=values)
    try:
        resp = urllib2.urlopen(req).read()
    except:
        raise Exception("error occur with url: %s" % url)
    return resp
