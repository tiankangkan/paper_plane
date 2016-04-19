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
from k_util.str_op import to_unicode, is_chinese, is_english, get_language, Language
from k_util.file_op import make_sure_file_dir_exists
from k_util.sound_op import SoundUtil
from k_util.time_op import get_time_str_now, TIME_FORMAT_FOR_FILE
from talker.talker_setting import TEMP_DIR
from paper_plane.proj_setting import MSG_TALKER_TRANSLATE
from paper_plane.settings import log_inst
from django.conf import settings


class Talker(object):
    def __init__(self, human_name='Lin', thinker_name='Alice', try_load_brain=True, use_site_package=False,
                 try_translate=True, response_time=0.01):
        self.human_name = human_name
        self.thinker_name = thinker_name
        self.thinker = aiml.Kernel()
        self.record_path = None
        self.speech_path = None
        self.thinker_sex = SpeechPeople.WOMAN    # 'MAN' or 'WOMAN'
        self.response_time = response_time
        self.sentence_trans = SentenceTranslator()
        self.tmp_path = os.path.join(TEMP_DIR, 'temp_master', 'talker')
        self.version = '1.0'
        self.saved_brain_path = os.path.join(self.tmp_path, 'saved_brain_%s.brn' % self.version)
        self.last_saved = 0
        self.auto_saved_period = 300
        self.use_site_package = use_site_package
        self.try_translate = try_translate
        self.load_thinker_with_aiml(try_load_brain=try_load_brain)

    def do_after_load_thinker(self):


    def load_thinker_with_aiml(self, try_load_brain=True):
        make_sure_file_dir_exists(self.saved_brain_path)
        if try_load_brain and os.path.isfile(self.saved_brain_path):
            self.thinker.bootstrap(brainFile=self.saved_brain_path)
        else:
            xml_file = self.get_aiml_startup_xml()
            if xml_file:
                cwd = os.getcwd()
                os.chdir(os.path.dirname(xml_file))
                self.thinker.learn(xml_file)
                self.thinker.respond("LOAD ALICE")
                self.thinker.saveBrain(self.saved_brain_path)
                self.last_saved = time.time()
                os.chdir(cwd)
        self.thinker.setBotPredicate('name', self.thinker_name)
        return self.thinker

    def set_human_name(self, human_name):
        self.human_name = human_name

    def set_thinker_name(self, thinker_name):
        self.thinker_name = thinker_name

    def get_aiml_startup_xml(self):
        if self.use_site_package:
            aiml_path = imp.find_module('aiml')[1]
            if not aiml:
                print "aiml path do not exist, please install it"
            xml_file = os.path.join(aiml_path, 'alice', 'startup.xml')
            print xml_file
        else:
            xml_file = os.path.join(settings.BASE_DIR, 'res', 'aiml-en-us-foundation-alice.v1-9', 'startup.xml')
        return xml_file

    def start(self):
        print '\n\n' + '=' * 30
        while True:
            human_msg = self.get_human_msg()
            # print 'TO   thinker: %s' % human_msg
            thinker_resp = self.thinker.respond(human_msg)
            # print 'FROM thinker: %s' % thinker_resp
            self.put_thinker_msg(thinker_resp=thinker_resp)
            sleep_time = random.uniform(0, 2*self.response_time)
            time.sleep(sleep_time)

    def respond_to_human_msg(self, msg, session_id=0, try_translate=None):
        try_translate = try_translate or self.try_translate
        if time.time() - self.last_saved > self.auto_saved_period:
            self.thinker.saveBrain(self.saved_brain_path)
        lang = get_language(msg)
        req_msg = to_unicode(msg)
        req_msg_t = req_msg
        if lang == Language.CN and try_translate:
            req_msg_t = self.sentence_trans.convert_to_en(msg)
        thinker_resp = self.thinker.respond(req_msg_t, sessionID=session_id)
        resp_msg = thinker_resp
        if lang == Language.CN:
            resp_msg = self.sentence_trans.convert_to_cn(thinker_resp)
        # print 'Ask: %s, Answer: %s' % (msg, thinker_resp)
        log_msg = '%s: [ID: %s] "%s" ->> "%s" ||->> "%s" ->> "%s"' % (session_id, MSG_TALKER_TRANSLATE, msg, req_msg_t, thinker_resp, resp_msg)
        log_inst.info(log_msg)
        return resp_msg

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
        human_msg = self.sentence_trans.convert_to_en(human_msg)
        return human_msg

    def put_thinker_msg(self, thinker_resp):
        thinker_resp_cn = self.sentence_trans.convert_to_cn(thinker_resp)
        thinker_msg = '\n%8s >> %s' % (self.thinker_name, thinker_resp_cn)
        print thinker_msg
        speech_name = 'speech_%s.mp3' % get_time_str_now(TIME_FORMAT_FOR_FILE)
        self.speech_path = os.path.join(TEMP_DIR, 'talker', 'audio', speech_name)
        make_sure_file_dir_exists(self.speech_path)
        speech_trans_inst.get_speech_of_text(thinker_resp_cn, to_file=self.speech_path, speech_sex=self.thinker_sex)
        time.sleep(0.01)
        sound_util = SoundUtil()
        sound_util.play_mp3(self.speech_path)


talker_inst = Talker(try_load_brain=True)


if __name__ == '__main__':
    talker = Talker(try_load_brain=False)
    talker.start()
    # talker.respond_to_human_msg(msg="what's your name")
    # talker.respond_to_human_msg(msg='你叫什么名字')


