# -*- coding: utf-8 -*-

from account.models import UserAccount

from paper_plane.url_manager import UrlManager
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
    save_user_to_db(wechat)
    content = wechat.message.content
    if u'飞机' in content or u'卖萌' in content:
        resp = handle_text_message_contains_paper_plane(wechat)
    else:
        resp = wechat.response_text(u'未匹配的输入哎', escape=False)
    return resp


def handle_text_message_contains_paper_plane(wechat):
    paper_plane_url = UrlManager().get_url_of_paper_plane()
    text = u'扔个纸飞机吧: %s' % paper_plane_url
    resp = wechat.response_text(text, escape=False)
    return resp
