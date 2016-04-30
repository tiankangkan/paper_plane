# -*- coding: utf-8 -*-

import json
import traceback
from models import WebPageInfo

from k_util.k_logger import log_inst
from k_util.str_op import to_unicode
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, HttpResponse


@csrf_exempt
def reply_to_one_page(request):
    return render_to_response('music_rss/one_page.html')


@csrf_exempt
def reply_to_one_page_get_more(request):
    try:
        item_list = list()
        web_pages = WebPageInfo.objects.all()
        page_values = web_pages.values()
        for page_item in page_values:
            item = json.loads(page_item['content'])
            desc_lines = to_unicode(item['desc'].replace('\n\n', '\n')).split("\n")
            item['desc'] = '<br/>'.join(desc_lines[:5])[:125]
            item_list.append(item)
        log_inst.info(json.dumps(item_list, indent=4))
        return HttpResponse(json.dumps(dict(status='success', msg=u'成功', item_list=item_list)))
    except Exception, e:
        print traceback.format_exc(e)
        return HttpResponse(json.dumps(dict(status='error', msg=u'(╯□╰) 这个世界需要再多一点爱')))


if __name__ == '__main__':
    reply_to_one_page('1234')
