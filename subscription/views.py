# -*- coding: utf-8 -*-
import json

from django.shortcuts import HttpResponse
from k_util.django_util import get_request_body
from k_util.http_util import post_request


def reply_to_token(request):
    # token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx03e221e02725c914&secret=f6cf7cbe34a977276bd74f3c6a60af61'
    # resp = post_request(token_url, method='GET')
    token = 'paper_plane_token'
    return HttpResponse(token)
