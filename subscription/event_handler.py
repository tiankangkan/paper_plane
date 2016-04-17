# -*- coding: utf-8 -*-

from account.models import UserAccount

from k_util.k_logger import logger


def save_user_to_db(wechat):
    wechat_openid = wechat.message.source
    queryset = UserAccount.objects.filter(wechat_openid=wechat_openid)
    if len(queryset) > 0:
        queryset.update(wechat_openid=wechat_openid)
    else:
        user = UserAccount.objects.create(wechat_openid=wechat_openid)
    logger.info('<save_user_to_db>: wechat_openid is %s' % wechat_openid)


def reply_to_text_message(wechat):
    content = wechat.message.content
    resp = 'received: %s' % content
    save_user_to_db(wechat)
    return wechat.response_text(resp, escape=False)

