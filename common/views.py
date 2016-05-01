# -*- coding: utf-8 -*-

import requests

from django.shortcuts import render_to_response, HttpResponse
from k_util.django_util import get_request_body


def reply_to_get_res_image(request):
    pass


def reply_to_agent(request):
    req = get_request_body(request)
    url = req['url']
    method = req.get('method', "GET")
    if method != 'POST':
        resp = requests.get(url)
        content = resp.content
        content_type = resp.headers['content-type']
        return HttpResponse(content=content, content_type=content_type)
    return HttpResponse("Error occur.")
