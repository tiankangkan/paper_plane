# -*- coding: UTF-8 -*-

"""
Desc: doc base.
Note:

---------------------------------------
# 2016/04/07   lin              created

"""

import aiml
import os
import imp
import time
import random

from sentence_translate import SentenceTranslator
from speech_translate import SPEECH_TRANSLATE
from k_util.str_op import to_unicode
from k_util.file_op import make_sure_file_dir_exists
from k_util.sound_op import SoundUtil
from k_util.time_op import get_time_str_now, TIME_FORMAT_FOR_FILE
from talker.talker_setting import TEMP_DIR


class Talker(object):
    def __init__(self, human_name='Lin', thinker_name='Alice', try_load_brain=True, response_time=0.01):
        self.thinker_name = thinker_name
        self.human_name = human_name
        self.thinker = None
        self.record_path = None
        self.speech_path = None
        self.thinker_sex = 'woman'    # 'man' or 'woman'
        self.response_time = response_time
        self.sentence_trans = SentenceTranslator()
        self.tmp_path = os.path.join(TEMP_DIR, 'temp_master', 'talker')
        self.saved_brain_path = os.path.join(self.tmp_path, 'saved_brain.brn')
        self.load_thinker_with_aiml(try_load_brain=try_load_brain)

    def load_thinker_with_aiml(self, try_load_brain=True):
        self.thinker = aiml.Kernel()
        make_sure_file_dir_exists(self.saved_brain_path)
        if os.path.isfile(self.saved_brain_path):
            self.thinker.bootstrap(brainFile=self.saved_brain_path)
        else:
            aiml_path = self.get_aiml_path()
            if aiml_path:
                aiml_res_path = os.path.join(aiml_path, 'standard')
                cwd = os.getcwd()
                os.chdir(aiml_res_path)
                startup_path = os.path.join(aiml_res_path, "startup.xml")
                self.thinker.learn(startup_path)
                self.thinker.respond("LOAD AIML B")
                self.thinker.saveBrain(self.saved_brain_path)
                os.chdir(cwd)
        return self.thinker

    def set_human_name(self, human_name):
        self.human_name = human_name

    def set_thinker_name(self, thinker_name):
        self.thinker_name = thinker_name

    def get_aiml_path(self):
        aiml_path = imp.find_module('aiml')[1]
        if not aiml:
            print "aiml path do not exist, please install it"
        return aiml_path

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

    def respond_to_human_msg(self, msg, session_id=0, keep_chinese=True):
        msg = to_unicode(msg)
        if keep_chinese:
            msg = self.sentence_trans.convert_to_en(msg)
        thinker_resp = self.thinker.respond(msg, sessionID=session_id)
        print type(msg), type(thinker_resp)
        if keep_chinese:
            thinker_resp = self.sentence_trans.convert_to_cn(thinker_resp)
        print type(msg), type(thinker_resp)
        # print 'Ask: %s, Answer: %s' % (msg, thinker_resp)
        return thinker_resp

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
            st = SPEECH_TRANSLATE
            human_msg = st.get_text_of_speech(self.record_path)
            human_print = '\n%8s >> %s' % (self.human_name, human_msg)
            print human_print
        human_msg = self.sentence_trans.convert_to_en(human_msg)
        return human_msg

    def put_thinker_msg(self, thinker_resp):
        thinker_resp_cn = self.sentence_trans.convert_to_cn(thinker_resp)
        thinker_msg = '\n%8s >> %s' % (self.thinker_name, thinker_resp_cn)
        print thinker_msg
        st = SPEECH_TRANSLATE
        speech_name = 'speech_%s.mp3' % get_time_str_now(TIME_FORMAT_FOR_FILE)
        self.speech_path = os.path.join(TEMP_DIR, 'talker', 'audio', speech_name)
        make_sure_file_dir_exists(self.speech_path)
        st.get_speech_of_text(thinker_resp_cn, to_file=self.speech_path, speech_sex=self.thinker_sex)
        time.sleep(0.01)
        sound_util = SoundUtil()
        sound_util.play_mp3(self.speech_path)


talker_inst = Talker(try_load_brain=False)


if __name__ == '__main__':
    talker = Talker()
    talker.start()


