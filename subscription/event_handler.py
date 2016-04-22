# -*- coding: utf-8 -*-

import StringIO
import json

from account.models import UserAccount
from mail_msg.models import MailMsg

from talker.speech_translate import speech_trans_inst, SpeechPeople
from talker.talker_main import talker_inst
from love_me.views import get_page_url_of_user_id
from k_util.str_op import to_utf_8
from paper_plane.proj_setting import MSG_LOVE_ME_REQUEST, MSG_WX_EVENT_FOLLOW, MSG_WX_EVENT_IGNORE
from paper_plane.settings import log_inst, DB_DIR
from k_util.key_value_store import KVStoreShelve


class WeChatMsgHandler(object):
    def __init__(self, wechat):
        self.wechat = wechat
        self.kv = KVStoreShelve(data_dir=DB_DIR, db_name='paper_plane')

    def save_user_to_db(self):
        wechat_openid = self.wechat.message.source
        queryset = UserAccount.objects.filter(wechat_openid=wechat_openid)
        if len(queryset) > 0:
            queryset.update(wechat_openid=wechat_openid)
        else:
            user = UserAccount.objects.create(wechat_openid=wechat_openid)
            user.save()
        log_inst.info('<save_user_to_db>: wechat_openid is %s' % wechat_openid)

    def query_from_mail_msg(self, t_type=None):
        source_id = self.wechat.message.source
        acc_obj = UserAccount.objects.get(wechat_openid=source_id)
        if t_type:
            queryset = MailMsg.objects.filter(target=acc_obj, t_type=t_type, is_read=False)
        else:
            queryset = MailMsg.objects.filter(target=acc_obj)
        msg_list = list(queryset.values()) if queryset else []
        queryset.update(is_read=True)
        return msg_list

    def get_love_me_review_mail(self):
        msg_list = self.query_from_mail_msg(t_type='love_me')
        if msg_list:
            msg_list.sort(key=lambda d: d['timestamp'])
        msg_list_show = list()
        for msg in msg_list:
            content_str = msg['content'] or '{}'
            content = json.loads(content_str)
            url = content['url']
            msg_str = '%s\n%s\n%s' % ('新到小飞机一枚 :)', '-'*15, url)
            msg_list_show.append(msg_str)
        return msg_list_show

    def reply_to_text_message(self):
        self.save_user_to_db()
        content = self.wechat.message.content
        if u'飞机' in content or u'卖萌' in content:
            resp_content = self.handle_text_message_contains_paper_plane()
        else:
            thinker_msg = self.handle_text_message_with_talker(human_msg=content)
            resp_content = to_utf_8(thinker_msg)
        msg_list_show = self.get_love_me_review_mail()
        if len(msg_list_show) > 0:
            msg = '\n\n'.join(msg_list_show)
            resp_content = msg + '\n%s\n' % ('-'*15) + resp_content
        resp = self.wechat.response_text(resp_content, escape=False)
        return resp

    def handle_rpc(self, resp_msg):
        t = talker_inst
        resp = ''
        if t.is_rpc(resp_msg):
            if t.rpc_type(resp_msg) == t.RPC_SET_EN_CN:
                self.set_english_chinese()
                resp = u'开启中英互译'
            elif t.rpc_type(resp_msg) == t.RPC_OFF_EN_CN:
                self.off_english_chinese()
                resp = u'关闭中英互译'
        return resp

    def set_english_chinese(self):
        session_id = self.wechat.message.source
        if session_id not in self.kv.inst:
            self.kv.put(session_id, dict())
        s = self.kv.get(session_id)
        s['mode_ch_en'] = 'ON'
        self.kv.sync()

    def off_english_chinese(self):
        session_id = self.wechat.message.source
        if session_id not in self.kv.inst:
            self.kv.put(session_id, dict())
        s = self.kv.get(session_id)
        s['mode_ch_en'] = 'OFF'
        self.kv.sync()

    def is_set_english_chinese(self):
        session_id = self.wechat.message.source
        return session_id in self.kv.inst and self.kv.inst[session_id]['mode_ch_en'] == 'ON'

    def is_off_english_chinese(self):
        session_id = self.wechat.message.source
        return session_id in self.kv.inst and self.kv.inst[session_id]['mode_ch_en'] == 'OFF'

    def handle_text_message_with_talker(self, human_msg):
        talker_inst.set_human_name(u'baby')
        thinker_msg = talker_inst.respond_to_human_msg(human_msg, try_translate=True, session_id=self.wechat.message.source)
        if self.is_set_english_chinese():
            thinker_msg = '%s\n%s\n%s' % (talker_inst.detail['resp_en'], '-'*10, talker_inst.detail['resp_cn'])
        if talker_inst.is_error_msg(thinker_msg):
            thinker_msg = u'电量快用尽了 💔 '
        log_inst.info('<reply_to_text_message>: Ask is %s, Answer is %s' % (to_utf_8(human_msg), to_utf_8(thinker_msg)))
        thinker_msg = thinker_msg
        return thinker_msg

    def handle_text_message_contains_paper_plane(self):
        log_msg = '%s: content: %s' % (MSG_LOVE_ME_REQUEST, self.wechat.message.content)
        log_inst.info(log_msg)
        url = get_page_url_of_user_id(self.wechat.message.source)
        # redirect_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%(app_id)s&redirect_uri=%(url)s&response_type=code&scope=snsapi_base'
        # redirect_url = redirect_url % (dict(app_id=wechat.conf.appid, url=url))
        return '飞一个纸飞机吧: \n%s' % url

    def reply_to_voice_message(self):
        self.save_user_to_db()
        media_id = self.wechat.message.media_id
        format = self.wechat.message.format
        recognition = self.wechat.message.recognition
        if not recognition:
            resp_content = u'没听清楚,再讲一遍可以吗? 😳 '
        else:
            resp_content = self.handle_text_message_with_talker(human_msg=recognition)
        log_inst.info('<reply_to_voice_message>: media_id: %s, format: %s, recognition: %s' % (media_id, format, recognition))
        return self.wechat.response_text(resp_content, escape=False)

    def reply_to_event_message(self):
        log_msg = '%s: type: %s, id: %s' % (MSG_WX_EVENT_IGNORE, self.wechat.message.type, self.wechat.message.source)
        log_inst.info(log_msg)
        if self.wechat.message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
            key = self.wechat.message.key                        # 对应于 XML 中的 EventKey (普通关注事件时此值为 None)
            ticket = self.wechat.message.ticket                  # 对应于 XML 中的 Ticket (普通关注事件时此值为 None)
            self.save_user_to_db()
            log_msg = '%s: id: %s' % (MSG_WX_EVENT_FOLLOW, self.wechat.message.source)
            log_inst.info(log_msg)
            return self.wechat.response_text(u'欢迎来到小康君的地盘, 由我们家可爱的Alice陪你聊天😊', escape=False)
        elif self.wechat.message.type == 'unsubscribe':  # 取消关注事件（无可用私有信息）
            pass
        elif self.wechat.message.type == 'scan':  # 用户已关注时的二维码扫描事件
            key = self.wechat.message.key                        # 对应于 XML 中的 EventKey
            ticket = self.wechat.message.ticket                  # 对应于 XML 中的 Ticket
        elif self.wechat.message.type == 'location':  # 上报地理位置事件
            latitude = self.wechat.message.latitude              # 对应于 XML 中的 Latitude
            longitude = self.wechat.message.longitude            # 对应于 XML 中的 Longitude
            precision = self.wechat.message.precision            # 对应于 XML 中的 Precision
        elif self.wechat.message.type == 'click':  # 自定义菜单点击事件
            key = self.wechat.message.key                        # 对应于 XML 中的 EventKey
        elif self.wechat.message.type == 'view':  # 自定义菜单跳转链接事件
            key = self.wechat.message.key                        # 对应于 XML 中的 EventKey
        elif self.wechat.message.type == 'templatesendjobfinish':  # 模板消息事件
            status = self.wechat.message.status                    # 对应于 XML 中的 Status
        elif self.wechat.message.type in ['scancode_push', 'scancode_waitmsg', 'pic_sysphoto',
                                     'pic_photo_or_album', 'pic_weixin', 'location_select']:  # 其他事件
            key = self.wechat.message.key                          # 对应于 XML 中的 EventKey
        return self.wechat.response_text(u'其实,其实,,, 这个功能目前还没有实现 ...', escape=False)

    def convert_text_to_voice_file_obj(self, text, sex):
        mp3_content = speech_trans_inst.get_speech_of_text(text=text, to_file=None, speech_sex=sex)
        file_obj = StringIO.StringIO()
        file_obj.write(mp3_content)
        file_obj.flush()
        file_obj.seek(0)
        return file_obj

    def upload_voice_message(self, file_path=None, file_obj=None, extension=''):
        media_file = file_path or file_obj
        if not media_file:
            raise ValueError('file_path and file_obj can not both be empty')
        else:
            resp = self.wechat.upload_media('voice', media_file, extension=extension)
            if file_obj:
                file_obj.closed()
            print resp
        return json.dumps(resp)

    def send_user_voice_message(self, text, sex=SpeechPeople.WOMAN):
        file_obj = self.convert_text_to_voice_file_obj(text, sex=sex)
        resp = self.upload_voice_message(file_obj=file_obj, extension='mp3')
        log_inst.info('<seed_voice_message>: resp: %s' % resp)
        return self.wechat.response_text(u'media_id: %s' % resp, escape=False)


if __name__ == '__main__':
    pass

