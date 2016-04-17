# -*- coding: utf-8 -*-


def reply_to_text_message(wechat):
    content = wechat.message.content
    resp = 'received: %s' % content
    return wechat.response_text(resp, escape=False)

