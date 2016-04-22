# -*- coding: UTF-8 -*-

"""
Desc: translate sentence.
Note:

---------------------------------------
# 2016/04/07   kangtian         created

"""

import urllib2
import json
from k_util.str_op import to_utf_8, chinese_percent, english_percent, is_english, is_chinese


class SentenceTranslator(object):
    TRANSLATION_ERROR = 'sentence translation error occur'

    def __init__(self):
        pass

    def convert_between_ch_and_en_with_youdao(self, sentence, host_name='Talker', app_key='1797213575'):
        if sentence == self.TRANSLATION_ERROR:
            return sentence + ''
        url_template = 'http://fanyi.youdao.com/openapi.do?keyfrom=%(host_name)s&key=%(app_key)s&type=data&doctype=json&version=1.1&q=%(sentence)s'
        sentence = to_utf_8(sentence)    # not support unicode
        sentence = urllib2.quote(sentence)
        url = url_template % {'host_name': host_name, 'app_key': app_key, 'sentence': sentence}
        req = urllib2.Request(url)
        resp_str = urllib2.urlopen(req, timeout=10).read()
        resp = json.loads(resp_str) if resp_str.startswith('{') else {}
        translation_list = resp.get('translation', [])
        translation = translation_list[0] if translation_list else self.TRANSLATION_ERROR
        if translation == self.TRANSLATION_ERROR:
            print 'Warning: TRANSLATION_ERROR occur'
        return translation

    def convert_to_en(self, sentence):
        if is_english(sentence, percent=1.0):
            return sentence
        translation_a = self.convert_between_ch_and_en_with_youdao(sentence)
        translation_b = self.convert_between_ch_and_en_with_youdao(translation_a)
        if english_percent(translation_a) > english_percent(translation_b):
            translation = translation_a
        else:
            translation = translation_b
        return translation

    def convert_to_cn(self, sentence):
        if is_chinese(sentence, percent=0.8):
            return sentence
        translation_a = self.convert_between_ch_and_en_with_youdao(sentence)
        translation_b = self.convert_between_ch_and_en_with_youdao(translation_a)
        if chinese_percent(translation_a) > chinese_percent(translation_b):
            translation = translation_a
        else:
            translation = translation_b
        return translation


if __name__ == '__main__':
    t = SentenceTranslator()
    # msg = raw_input('input: ')
    print t.convert_to_cn(u'你好吗？')

