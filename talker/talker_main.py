# -*- coding: UTF-8 -*-

"""
Desc: doc base.
Note:

---------------------------------------
# 2016/04/07   lin              created

"""
import paper_plane.django_init
import aiml
import os
import imp
import time
import random

from sentence_translate import SentenceTranslator
from speech_translate import speech_trans_inst, SpeechPeople
from k_util.str_op import to_unicode, to_utf_8, is_chinese_char, is_ascii_char, get_language, Language
from k_util.file_op import make_sure_file_dir_exists
from k_util.sound_op import SoundUtil
from k_util.time_op import get_time_str_now, TIME_FORMAT_FOR_FILE
from talker.talker_setting import TEMP_DIR
from paper_plane.proj_setting import MSG_TALKER_TRANSLATE
from paper_plane.settings import log_inst
from django.conf import settings


class Talker(object):
    RPC_NOT_MATCH = 'RPC NOTXXMATCH'
    RPC_SET_EN_CN = 'RPC SETXXENXXCN'
    RPC_OFF_EN_CN = 'RPC OFFXXENXXCN'
    RPC_UNKNOWN = 'RPC UNKNOWN'

    rpc_type = {
        'RPC NOTXXMATCH': RPC_NOT_MATCH,
        'RPC SETXXENXXCN': RPC_SET_EN_CN,
        'RPC OFFXXENXXCN': RPC_OFF_EN_CN
    }

    def __init__(self, human_name='Lin', thinker_name='Alice', try_load_brain=True, use_site_package=False,
                 try_translate=True, response_time=0.01, xml_path=None, load=None):
        self.human_name = human_name
        self.thinker_name = thinker_name
        self.thinker = aiml.Kernel()
        self.record_path = None
        self.speech_path = None
        self.thinker_sex = SpeechPeople.WOMAN    # 'MAN' or 'WOMAN'
        self.response_time = response_time
        self.xml_path = xml_path
        self.load = None
        self.sentence_trans = SentenceTranslator(way=SentenceTranslator.WAY_BAIDU)
        self.tmp_path = os.path.join(TEMP_DIR, 'brain')
        self.version = '1.0'    # 改变 version 来重新加载大脑数据
        self.saved_brain_path = os.path.join(self.tmp_path, 'saved_brain_%s.brn' % self.version)
        self.last_saved = 0
        self.auto_saved_period = 300
        self.use_site_package = use_site_package
        self.try_translate = try_translate
        self.session_id_now = 0
        self.detail = dict(
            req_cn=None, req_en=None,
            resp_cn=None, resp_en=None
        )
        self.empty_msg = u'很抱歉, 不能回答你, 我会成长起来的.. 🌹 '
        self.load_thinker_with_aiml(try_load_brain=try_load_brain)

    def load_thinker_with_aiml(self, try_load_brain=True):
        make_sure_file_dir_exists(self.saved_brain_path)
        if try_load_brain and os.path.isfile(self.saved_brain_path):
            self.thinker.bootstrap(brainFile=self.saved_brain_path)
        else:
            xml_file = self.get_aiml_startup_xml()
            load = self.load or "LOAD ALICE"
            if xml_file:
                cwd = os.getcwd()
                os.chdir(os.path.dirname(xml_file))
                self.thinker.learn(xml_file)
                self.thinker.respond(load)
                self.thinker.saveBrain(self.saved_brain_path)
                self.last_saved = time.time()
                os.chdir(cwd)
        self.thinker.setBotPredicate('name', self.thinker_name)
        return self.thinker

    def set_human_name(self, human_name):
        self.human_name = human_name

    def set_thinker_name(self, thinker_name):
        self.thinker_name = thinker_name

    @staticmethod
    def add_space_between_cn_char(msg):
        uni_msg = to_unicode(msg)
        uni_msg_temp = ''.join([' %s ' % ch if is_chinese_char(ch) else ch for ch in uni_msg])
        msg = ' '.join(uni_msg_temp.split())
        if isinstance(msg, str):
            msg = to_utf_8(uni_msg)
        return msg

    def get_aiml_startup_xml(self):
        if self.xml_path:
            return self.xml_path
        if self.use_site_package:
            aiml_path = imp.find_module('aiml')[1]
            if not aiml:
                print "aiml path do not exist, please install it"
            xml_file = os.path.join(aiml_path, 'standard', 'startup.xml')
            print xml_file
        else:
            xml_file = os.path.join(settings.BASE_DIR, 'res', 'aiml-en-us-foundation-alice.v1-9', 'startup.xml')
        return xml_file

    def start(self):
        print '\n\n' + '=' * 30
        while True:
            human_msg = self.get_human_msg()
            print 'TO   thinker: %s' % human_msg
            thinker_resp = self.respond_to_msg(human_msg)
            print 'FROM thinker: %s' % thinker_resp
            self.put_thinker_msg(thinker_resp=thinker_resp)
            sleep_time = random.uniform(0, 2*self.response_time)
            time.sleep(sleep_time)

    def is_un_escape(self, msg):
        return msg.lower().startswith('rpc ')

    def is_rpc(self, msg):
        return msg.lower().startswith('rpc ')

    def get_rpc_type(self, msg):
        rpc = msg.upper()
        return self.rpc_type.get(rpc, self.RPC_UNKNOWN)

    def respond_to_human_msg(self, msg, session_id=None, try_translate=None):
        if session_id is not None:
            self.session_id_now = session_id
        if try_translate is None:
            try_translate = self.try_translate
        # if not try_translate:
        #     msg = self.add_space_between_cn_char(msg)
        #     print msg
        if time.time() - self.last_saved > self.auto_saved_period:
            self.thinker.saveBrain(self.saved_brain_path)
        lang = get_language(msg)
        req_msg = to_unicode(msg)
        req_msg_t = req_msg
        print lang, try_translate
        if lang == Language.CN and try_translate:
            req_msg_t = self.sentence_trans.convert_to_en(req_msg)
        thinker_resp = self.thinker.respond(req_msg_t, sessionID=session_id)
        if self.is_un_escape(thinker_resp):
            if self.is_rpc(thinker_resp):
                resp_msg = self.handle_rpc(req_msg, thinker_resp)
        else:
            if len(thinker_resp) == 0:
                thinker_resp = self.empty_msg
            resp_msg = thinker_resp
            if lang == Language.CN:
                resp_msg = self.sentence_trans.convert_to_cn(thinker_resp)
            resp_msg = resp_msg if resp_msg else self.empty_msg
        log_msg = '%s: [ID: %s] "%s" ->> "%s" ||->> "%s" ->> "%s"' % (MSG_TALKER_TRANSLATE, session_id, msg, req_msg_t, thinker_resp, resp_msg)
        log_inst.info(log_msg)
        return resp_msg

    def handle_rpc(self, msg_req, msg_resp):
        if msg_resp == self.RPC_NOT_MATCH and msg_req != self.RPC_NOT_MATCH:
            new_msg = self.sentence_trans.convert_to_en(msg_req)
            print 'RPC_NOT_MATCH, %s -> %s' % (msg_req, new_msg)
            msg_resp = self.respond_to_human_msg(msg=new_msg, session_id=self.session_id_now)
        return msg_resp

    def set_detail(self, msg, lang, role):
        import copy
        msg = copy.deepcopy(msg)
        if lang == Language.CN and role == 'req':
            self.detail['req_cn'] = msg
        elif lang == Language.EN and role == 'req':
            self.detail['req_en'] = msg
        elif lang == Language.CN and role == 'resp':
            self.detail['resp_cn'] = msg
        elif lang == Language.EN and role == 'resp':
            self.detail['resp_en'] = msg

    def clean_detail(self):
        self.detail['req_cn'], self.detail['req_en'] = None, None
        self.detail['resp_cn'], self.detail['resp_en'] = None, None

    def makeup_detail(self):
        if not self.detail['req_cn']:
            self.detail['req_cn'] = self.sentence_trans.convert_to_cn(self.detail['req_en'])
        if not self.detail['req_en']:
            self.detail['req_en'] = self.sentence_trans.convert_to_en(self.detail['req_cn'])
        if not self.detail['resp_cn']:
            self.detail['resp_cn'] = self.sentence_trans.convert_to_cn(self.detail['resp_en'])
        if not self.detail['resp_en']:
            self.detail['resp_en'] = self.sentence_trans.convert_to_en(self.detail['resp_cn'])

    def respond_to_msg(self, msg, session_id=None):
        req_msg = to_unicode(msg)
        lang = get_language(req_msg)
        self.clean_detail()
        self.set_detail(req_msg, lang, 'req')
        if session_id is not None:
            self.session_id_now = session_id
        if time.time() - self.last_saved > self.auto_saved_period:
            self.thinker.saveBrain(self.saved_brain_path)
        resp_temp = self.thinker.respond(req_msg, sessionID=session_id)
        self.set_detail(resp_temp, get_language(resp_temp), 'resp')
        print '%s -->> %s' % (req_msg, resp_temp)
        req_msg_en = 'DO NOT NEED TRANSLATE'
        if self.get_rpc_type(resp_temp) == self.RPC_NOT_MATCH and lang == Language.CN:
            req_msg_en = self.sentence_trans.convert_to_en(req_msg)
            resp_temp = self.thinker.respond(req_msg_en, sessionID=session_id)
            self.set_detail(req_msg_en, Language.EN, 'resp')
            self.set_detail(resp_temp, get_language(resp_temp), 'resp')
        if self.is_un_escape(resp_temp):
            resp = resp_temp
        else:
            req_lang, resp_lang = get_language(req_msg), get_language(resp_temp)
            if req_lang != resp_lang:
                if req_lang == Language.EN:
                    resp = self.sentence_trans.convert_to_en(resp_temp)
                else:
                    resp = self.sentence_trans.convert_to_cn(resp_temp)
            else:
                resp = resp_temp
        self.set_detail(resp, get_language(resp), 'resp')
        log_msg = '%s: [ID: %s] "%s" ->> "%s" ||->> "%s" ->> "%s"' % (MSG_TALKER_TRANSLATE, session_id, req_msg, req_msg_en, resp_temp, resp)
        log_inst.info(log_msg)
        return resp

    def shutdown(self):
        self.thinker.saveBrain(self.saved_brain_path)

    def get_human_msg(self):
        human_hint = '\n%8s >> ' % self.human_name
        human_msg = raw_input(human_hint)
        if human_msg in (' ', '\n', '\r\n', ''):
            sound_util = SoundUtil()
            record_name = 'record_%s.wav' % get_time_str_now(TIME_FORMAT_FOR_FILE)
            self.record_path = os.path.join(TEMP_DIR, 'talker', 'audio', record_name)
            make_sure_file_dir_exists(self.record_path)
            sound_util.start_record_wave(file_path=self.record_path)
            _ = raw_input('\n%8s >> %s' % ('system', 'Please speech ... Enter to stop'))
            sound_util.stop_record_wave()
            time.sleep(0.01)
            human_msg = speech_trans_inst.get_text_of_speech(self.record_path)
            human_print = '\n%8s >> %s' % (self.human_name, human_msg)
            print human_print
        return human_msg

    def put_thinker_msg(self, thinker_resp):
        thinker_msg = '\n%8s >> %s' % (self.thinker_name, thinker_resp)
        print thinker_msg
        speech_name = 'speech_%s.mp3' % get_time_str_now(TIME_FORMAT_FOR_FILE)
        self.speech_path = os.path.join(TEMP_DIR, 'talker', 'audio', speech_name)
        make_sure_file_dir_exists(self.speech_path)
        speech_trans_inst.get_speech_of_text(thinker_resp, to_file=self.speech_path, speech_sex=self.thinker_sex)
        time.sleep(0.01)
        sound_util = SoundUtil()
        sound_util.play_mp3(self.speech_path)

    def is_error_msg(self, msg):
        return self.sentence_trans.is_error_msg(msg)


talker_inst = Talker(try_load_brain=True)    # 不要更改这里的设置, 可能会丢失大脑保存的数据


if __name__ == '__main__':
    # talker = Talker(try_load_brain=False, use_site_package=True, xml_path='/Users/kangtian/Documents/Master/paper_plane/res/aiml_master_v0.0/cn-startup.xml', load='LOAD ALICE')
    talker = Talker(try_load_brain=False, try_translate=False)
    talker.start()
    # talker.respond_to_human_msg(msg="what's your name")
    # talker.respond_to_human_msg(msg='你叫什么名字')


