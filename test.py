#/usr/bin/env python
#coding=utf8

import requests

resp = requests.get('http://img6.douban.com/view/presto/large/public/t114876.jpg')
print resp.headers['content-type']

print 'hello'
