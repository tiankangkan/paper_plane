# -*- coding: utf-8 -*-

from account.models import UserAccount
from wechat_sdk import WechatBasic

from paper_plane.url_manager import UrlManager
from talker.talker_main import talker_inst
from k_util.k_logger import logger
from k_util.str_op import to_utf_8


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
        talker_inst.set_human_name(u'baby')
        thinker_msg = talker_inst.respond_to_human_msg(content, keep_chinese=True, session_id=wechat.message.source)
        logger.info('<reply_to_text_message>: Ask is %s, Answer is %s' % (to_utf_8(content), to_utf_8(thinker_msg)))
        thinker_msg = to_utf_8(thinker_msg)
        resp = wechat.response_text(thinker_msg, escape=False)
    return resp


def handle_text_message_contains_paper_plane(wechat):
    paper_plane_url = UrlManager().get_url_of_paper_plane()
    text = u'扔个纸飞机吧: %s' % paper_plane_url
    resp = wechat.response_text(text, escape=False)
    return resp


def reply_to_voice_message(wechat):
    save_user_to_db(wechat)
    media_id = wechat.message.media_id
    format = wechat.message.format
    recognition = wechat.message.recognition
    if not recognition:
        resp_content = u'没听清楚,再讲一遍可以吗? 😳 '
    else:
        resp_content = handle_text_message_contains_paper_plane(recognition)
    logger.info('<reply_to_voice_message>: media_id: %s, format: %s, recognition: %s' % (media_id, format, recognition))
    return wechat.response_text(resp_content, escape=False)


def reply_to_event_message(wechat):
    if wechat.message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
        key = wechat.message.key                        # 对应于 XML 中的 EventKey (普通关注事件时此值为 None)
        ticket = wechat.message.ticket                  # 对应于 XML 中的 Ticket (普通关注事件时此值为 None)
        save_user_to_db(wechat)
        return wechat.response_text(u'欢迎来到小康君的地盘, 由我们家可爱Alice陪你聊天哦', escape=False)
    elif wechat.message.type == 'unsubscribe':  # 取消关注事件（无可用私有信息）
        pass
    elif wechat.message.type == 'scan':  # 用户已关注时的二维码扫描事件
        key = wechat.message.key                        # 对应于 XML 中的 EventKey
        ticket = wechat.message.ticket                  # 对应于 XML 中的 Ticket
    elif wechat.message.type == 'location':  # 上报地理位置事件
        latitude = wechat.message.latitude              # 对应于 XML 中的 Latitude
        longitude = wechat.message.longitude            # 对应于 XML 中的 Longitude
        precision = wechat.message.precision            # 对应于 XML 中的 Precision
    elif wechat.message.type == 'click':  # 自定义菜单点击事件
        key = wechat.message.key                        # 对应于 XML 中的 EventKey
    elif wechat.message.type == 'view':  # 自定义菜单跳转链接事件
        key = wechat.message.key                        # 对应于 XML 中的 EventKey
    elif wechat.message.type == 'templatesendjobfinish':  # 模板消息事件
        status = wechat.message.status                    # 对应于 XML 中的 Status
    elif wechat.message.type in ['scancode_push', 'scancode_waitmsg', 'pic_sysphoto',
                                 'pic_photo_or_album', 'pic_weixin', 'location_select']:  # 其他事件
        key = wechat.message.key                          # 对应于 XML 中的 EventKey
    return wechat.response_text(u'其实,其实,,, 这个功能目前还没有实现 ...', escape=False)
