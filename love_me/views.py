# -*- coding: utf-8 -*-

import json
import random
import datetime
import urllib
import pytz
import traceback

from models import ConversationPage
from account.models import UserAccount
from django.shortcuts import render_to_response, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from paper_plane.url_manager import UrlManager
from k_util.django_util import get_request_body


def reply_to_show_form(request):
    print '====================   get req   ===================='
    return render_to_response('show_form.html')


@csrf_exempt
def reply_to_paper_plane(request):
    req = get_request_body(request)
    print json.dumps(req, indent=4)
    extra_source_id = req.get('extra_source_id', None)
    pic_name = req.get('pic_name', '0001.jpg')
    t_id = req.get('t_id', None)
    t_id = int(t_id) if t_id else None
    values = dict(pic_name=pic_name, extra_source_id=extra_source_id, t_id=t_id)
    return render_to_response('paper_plane.html', {'values': json.dumps(values)})


@csrf_exempt
def reply_to_paper_plane_do_submit(request):
    req = get_request_body(request)
    print json.dumps(req, indent=4)
    extra_source_id = req.get('extra_source_id', None)
    how_much_love = req.get('how_much_love', None)
    when_begin_love = req.get('when_begin_love', None)
    want_to_say = req.get('want_to_say', None)
    pic_name = req.get('pic_name', "0001.jpg")
    t_id = req.get('t_id', None)
    t_id = int(t_id) if t_id else None
    # if not (t_id and extra_source_id):
    #     return HttpResponse(json.dumps(dict(status='error', msg=u'未确定的网页来源...')))
    content_dict = dict(
        how_much_love=how_much_love,
        when_begin_love=when_begin_love,
        want_to_say=want_to_say,
        pic_name=pic_name,
        extra_source_id=extra_source_id
    )
    print 'id is %s' % t_id
    print json.dumps(content_dict, indent=4)
    update_conversation_page_db(t_id=t_id, source_id=extra_source_id, content_dict=content_dict, is_read=True)
    return HttpResponse(json.dumps(dict(status='success', msg=u'成功')))


@csrf_exempt
def update_conversation_page_db(t_id=None, source_id=None, target_id=None, content_dict=None, is_read=False):
    try:
        content_dict = content_dict or dict()
        print 'source_id...', source_id, target_id
        source = UserAccount.objects.get(wechat_openid=source_id) if source_id else None
        target = UserAccount.objects.get(wechat_openid=target_id) if target_id else None
        values = dict(
            source=source,
            target=target,
            timestamp=datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)),
            content=json.dumps(content_dict),
            is_read=is_read,
        )
        if t_id:
            obj = ConversationPage.objects.get(t_id=t_id)
            obj = obj.update(*values)
            # obj = ConversationPage.objects.create(**values)
        else:
            obj = ConversationPage.objects.create(**values)
        return obj
    except Exception, e:
        print traceback.format_exc(e)
    return HttpResponse(json.dumps(dict(status='success', msg=u'成功')))


@csrf_exempt
def reply_text_message_contains_paper_plane(extra_source_id):
    paper_plane_url = UrlManager().get_url_of_paper_plane()
    pic_name = '%4.4d.jpg' % random.randrange(start=1, stop=10)
    content_dict = dict(extra_source_id=extra_source_id, pic_name=pic_name)
    obj = update_conversation_page_db(source_id=extra_source_id, content_dict=content_dict, is_read=False)
    content_dict['t_id'] = obj.t_id
    para_str = urllib.urlencode(content_dict)
    paper_plane_url = '%s?%s' % (paper_plane_url, para_str)
    text = u'扔个纸飞机吧: %s' % paper_plane_url
    return text
