# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup

import requests

resp = requests.get('http://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&tn=baidu&wd=requests&oq=request&rsv_pq=bb452ffd00013ca7&rsv_t=c892Oi%2FvYdYLWd7FY6RT1OaPnfrnDqDqM9TEwwRWPlWcVMrWrOW8Z8LQv2Q&rsv_enter=1&inputT=1251&rsv_sug3=83&rsv_sug1=71&rsv_sug7=100&rsv_sug2=0&prefixsug=request&rsp=0&rsv_sug4=2787')

html = resp.text

soup = BeautifulSoup(html)
print soup.get_text()
