# -*- coding: utf-8 -*-

import json
import datetime
import traceback
from models import WebPageInfo
import tzlocal

from k_util.k_logger import log_inst
from k_util.str_op import to_unicode
from k_util.django_util import get_request_body
from k_util.time_op import convert_time_str_to_time_obj, convert_time_obj_to_time_str, TZ_UTC, get_time_str_unique, TIME_FORMAT_FOR_FILE
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, HttpResponse


@csrf_exempt
def reply_to_one_page(request):
    return render_to_response('music_rss/one_page.html')


@csrf_exempt
def reply_to_one_page_get_more(request):
    try:
        req = get_request_body(request)
        update_time_str = req.get('update_time_str', '')
        item_num = req.get('item_num', 10)
        default_update_time = datetime.datetime(year=2100, month=1, day=1)
        default_update_time_str = get_time_str_unique(time_obj=default_update_time, time_format=TIME_FORMAT_FOR_FILE)
        update_time_str = update_time_str or default_update_time_str
        item_list = list()
        web_pages = WebPageInfo.objects.filter(update_time_str__lt=update_time_str).order_by('-update_time_str')[:item_num]
        page_values = web_pages.values()
        for page_item in page_values:
            item = json.loads(page_item['content'])
            desc_lines = to_unicode(item['desc'].replace('\n\n', '\n')).split("\n")
            item['desc'] = '<br/>'.join(desc_lines[:5])[:125]
            item['update_time'] = convert_time_obj_to_time_str(page_item['update_time'])
            log_inst.info(page_item['update_time_str'])
            item_list.append(item)
        log_inst.info(update_time_str + json.dumps(item_list, indent=4))
        return HttpResponse(json.dumps(dict(status='success', msg=u'成功', item_list=item_list)))
    except Exception, e:
        print traceback.format_exc(e)
        return HttpResponse(json.dumps(dict(status='error', msg=u'(╯□╰) 这个世界需要再多一点爱')))


if __name__ == '__main__':
    reply_to_one_page('1234')
