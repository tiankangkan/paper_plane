# -*- coding: utf-8 -*-

import json
from wechat_sdk import messages
from wechat_sdk import WechatBasic

from django.utils.encoding import smart_str
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from k_util.k_logger import logger
import event_handler


wechat = WechatBasic(
    token='masterkang',
    appid='wx03e221e02725c914',
    appsecret='f6cf7cbe34a977276bd74f3c6a60af61'
)


@csrf_exempt
def weixin_entry(request):
    """
    所有的消息都会先进入这个函数进行处理，函数包含两个功能，
    微信接入验证是GET方法，
    微信正常的收发消息是用POST方法。
    """
    if request.method == "GET":
        logger.info('IN weixin_entry ==================')
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        result = wechat.check_signature(signature, timestamp, nonce)
        if result:
            return HttpResponse(echostr)
        else:
            return HttpResponse("weixin  index")
    else:
        xml_str = smart_str(request.body)
        logger.info('xml_str:\n%s' % xml_str)
        wechat.parse_data(xml_str)
        resp = dispatch_event(wechat)
        return HttpResponse(resp)


def dispatch_event(wechat):
    if isinstance(wechat.message, messages.TextMessage):
        return event_handler.reply_to_text_message(wechat)
    else:
        return wechat.response_text('Unsupported Msg Type', escape=False)
