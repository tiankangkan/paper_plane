# -*- coding: utf-8 -*-

import requests
import json
import os
import random
from k_util.django_util import get_request_body
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, HttpResponse
from paper_plane.url_manager import UrlManager
from models import FileMapping

BT_FILE_NUM = len(FileMapping.objects.all())


@csrf_exempt
def reply_to_treasure(request):
    req = get_request_body(request)
    parameter = dict(identify=req['id'])
    return render_to_response('treasure/open_treasure.html', dict(parameter=json.dumps(parameter)))


@csrf_exempt
def reply_to_treasure_get_url(request):
    req = get_request_body(request)
    identify = req['identify']
    f_item = FileMapping.objects.get(identify=identify)
    file_path = f_item.file_path
    sub_path = os.path.join('bt', os.path.basename(file_path))
    resp = dict(url='/treasure/res_treasure/%s' % sub_path)
    return HttpResponse(json.dumps(resp))


@csrf_exempt
def reply_to_treasure_get_random(request):
    resp = get_treasure()
    return HttpResponse(json.dumps(resp))


def get_treasure():
    item_list = [u'海星', u'海豚', u'金鱼']
    hit_rate = 0.5
    number = random.uniform(0.0, 1.0)
    if number < hit_rate:
        content = get_url_of_random_bt()
        treasure = dict(content=content, type='bt')
    else:
        content = random.choice(item_list)
        treasure = dict(content=content, type='thanks')
    return treasure


def get_url_of_random_bt():
    treasure_url = UrlManager().get_treasure_url()
    random.randint(0, BT_FILE_NUM)
    ids = FileMapping.objects.values_list('id', flat=True)
    random_id = random.choice(ids)
    item = FileMapping.objects.get(id=random_id)
    treasure_url += '?id=%s' % item.identify
    return treasure_url
