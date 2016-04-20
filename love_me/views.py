# -*- coding: utf-8 -*-
import paper_plane.django_init
import json
import random
import datetime
import urllib
import traceback
import os

from love_me.models import ConversationPage
from account.models import UserAccount
from django.shortcuts import render_to_response, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from paper_plane.url_manager import UrlManager
from paper_plane.file_manager import FileManager
from paper_plane.proj_setting import MSG_LOVE_ME_REQUEST, MSG_LOVE_ME_SUBMIT
from paper_plane.settings import log_inst, IMAGE_RES
from k_util.django_util import get_request_body
from k_util.qrcode_util import make_qrcode
from k_util.time_op import get_time_str_now_for_file


@csrf_exempt
def reply_to_paper_plane(request):
    req = get_request_body(request)
    log_msg = '%s: %s' % (MSG_LOVE_ME_REQUEST, json.dumps(req, indent=4))
    log_inst.info(log_msg)
    extra_source_id = req.get('extra_source_id', None)
    pic_name = req.get('pic_name', '0001.jpg')
    values = dict(pic_name=pic_name, extra_source_id=extra_source_id)
    return render_to_response('paper_plane_sender.html', {'values': json.dumps(values)})


@csrf_exempt
def reply_to_paper_plane_sender_do_submit_old(request):
    req = get_request_body(request)
    log_msg = '%s: %s' % (MSG_LOVE_ME_SUBMIT, json.dumps(req, indent=4))
    log_inst.info(log_msg)
    extra_source_id = req.get('extra_source_id', None)
    how_much_love = req.get('how_much_love', None)
    when_begin_love = req.get('when_begin_love', None)
    want_to_say = req.get('want_to_say', None)
    pic_name = req.get('pic_name', "0001.jpg")
    t_id = req.get('t_id', None)
    t_id = int(t_id) if t_id else None
    if not t_id:
        return HttpResponse(json.dumps(dict(status='error', msg=u'未确定的网页来源...')))
    content_dict = dict(
        how_much_love=how_much_love,
        when_begin_love=when_begin_love,
        want_to_say=want_to_say,
        pic_name=pic_name,
        extra_source_id=extra_source_id
    )
    update_conversation_page_db(t_id=t_id, source_id=extra_source_id, content_dict=content_dict, is_read=True)
    return HttpResponse(json.dumps(dict(status='success', msg=u'成功')))


@csrf_exempt
def reply_to_paper_plane_sender_do_submit(request):
    try:
        req = get_request_body(request)
        log_msg = '%s: %s' % (MSG_LOVE_ME_SUBMIT, json.dumps(req, indent=4))
        log_inst.info(log_msg)
        field_list = ['nick_name', 'how_much_love', 'when_begin_love', 'when_begin_love', 'want_to_say', 'extra_0_question', 'receiver_url', 'pic_name', 'extra_source_id']
        req_dict = dict()
        for field in field_list:
            req_dict[field] = req.get(field, None)

        content_dict = dict(
            how_much_love=req_dict['how_much_love'],
            when_begin_love=req_dict['when_begin_love'],
            want_to_say=req_dict['want_to_say'],
            pic_name=req_dict['pic_name'],
            extra_source_id=req_dict['extra_source_id']
        )
        db_obj = update_conversation_page_db(source_id=req_dict['extra_source_id'], content_dict=content_dict, is_read=True)
        qrcode_id = 'qrcode_%s.png' % get_time_str_now_for_file()
        qrcode_path = FileManager().get_path_of_qrcode(res_id=qrcode_id)
        receiver_url = req_dict['receiver_url'] + '&t_id=%s' % db_obj.t_id
        make_qrcode(receiver_url, qrcode_path)
        qrcode_url = UrlManager().get_url_of_qrcode(qrcode_id)
        return HttpResponse(json.dumps(dict(status='success', msg=u'成功', qrcode_url=qrcode_url)))
    except Exception, e:
        print traceback.format_exc(e)
        return HttpResponse(json.dumps(dict(status='error', msg=u'(╯□╰) 这个世界需要再多一点爱')))


@csrf_exempt
def update_conversation_page_db(source_id=None, target_id=None, content_dict=None, is_read=False):
    obj = None
    try:
        content_dict = content_dict or dict()
        print 'source_id: %s, target_id: %s' % (source_id, target_id)
        try:
            source = UserAccount.objects.get(wechat_openid=source_id) if source_id else None
        except:
            source = UserAccount.objects.create(wechat_openid=source_id).save()
        try:
            target = UserAccount.objects.get(wechat_openid=target_id) if target_id else None
        except:
            target = UserAccount.objects.create(wechat_openid=target_id).save()
        values = dict(
            source=source,
            target=target,
            content=json.dumps(content_dict),
            is_read=is_read,
            timestamp=datetime.datetime.now(),
        )
        obj = ConversationPage.objects.create(**values).save()
    except Exception, e:
        print traceback.format_exc(e)
    return obj


@csrf_exempt
def reply_text_message_contains_paper_plane(extra_source_id):
    paper_plane_url = UrlManager().get_url_of_paper_plane()
    pic_name = '%4.4d.jpg' % random.randrange(start=1, stop=10)
    content_dict = dict(extra_source_id=extra_source_id, pic_name=pic_name)
    para_str = urllib.urlencode(content_dict)
    paper_plane_url = '%s?%s' % (paper_plane_url, para_str)
    text = u'扔个纸飞机吧: %s' % paper_plane_url
    return text


if __name__ == '__main__':
    reply_text_message_contains_paper_plane(1123)
