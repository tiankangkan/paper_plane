# -*- coding: utf-8 -*-

import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, HttpResponse
from models import FileMapping


@csrf_exempt
def reply_to_treasure(request):
    return render_to_response('treasure/open_treasure.html')


@csrf_exempt
def reply_to_treasure_get_url(request):
    resp = dict(url='/treasure/res_treasure/test.torrent')
    return HttpResponse(json.dumps(resp))
