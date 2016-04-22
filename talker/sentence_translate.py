# -*- coding: UTF-8 -*-

"""
Desc: translate sentence.
Note:

---------------------------------------
# 2016/04/07   kangtian         created

"""

import urllib2, urllib
import json
import random
import hashlib

from k_util.str_op import to_utf_8, chinese_percent, english_percent, is_english, is_chinese


class SentenceTranslatorBaidu(object):
    SUCCESS = 'success'
    ERR_TIMEOUT = 'request timeout'
    ERR_FREQUENCY = 'request frequency limited'
    ERR_TOO_LONG = 'query is too long'
    ERR_LANG = 'not support the language'
    ERR_EMPTY = 'the result is empty'
    ERR_UN_KNOWN = 'un known error occur'
    error_msg = {
        '52000': SUCCESS,
        '52001': ERR_TIMEOUT,
        '54003': ERR_FREQUENCY,
        '54005': ERR_TOO_LONG,
        '58001': ERR_LANG,
        '54000': ERR_EMPTY
    }

    LANG_EN = 'en'
    LANG_CN = 'zh'

    def __init__(self, app_id=None, key=None):
        self.app_id = app_id or '20160422000019400'
        self.key = key or 'zKYg5i69FHulvWDQsJ7m'
        self.url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

    def is_error_msg(self, msg):
        return msg in (self.ERR_EMPTY, self.ERR_FREQUENCY, self.ERR_LANG, self.ERR_TIMEOUT, self.ERR_TOO_LONG, self.ERR_UN_KNOWN)

    def post_request(self, sentence, to_lang, from_lang='auto'):
        sentence = to_utf_8(sentence)
        salt = random.randrange(0, 10000),
        str_check = self.app_id + sentence + str(salt) + self.key
        m2 = hashlib.md5()
        m2.update(str_check)
        sign = m2.hexdigest()
        query_dict = {
            'q': sentence,
            'salt': salt,
            'appid': self.app_id,
            'from': from_lang,
            'to': to_lang,
            'sign': sign
        }
        full_url = self.url + '?' + urllib.urlencode(query_dict)
        req = urllib2.Request(full_url)
        resp_str = urllib2.urlopen(req).read()
        resp = json.loads(resp_str)
        error_code = resp.get('error_code', '52000')
        if error_code != '52000':
            error_msg = self.error_msg.get(error_code, 'Un know error: %s' % error_code)
            result = error_msg
        else:
            result_both = resp.get('trans_result', {})
            print result_both
            if result_both:
                result = result_both[0].get('dst', self.ERR_EMPTY)
            else:
                result = self.ERR_UN_KNOWN
        return result

    def convert_to_en(self, sentence):
        result = self.post_request(sentence, to_lang=self.LANG_EN)
        return result

    def convert_to_cn(self, sentence):
        result = self.post_request(sentence, to_lang=self.LANG_CN)
        return result


class SentenceTranslatorYouDao(object):
    TRANSLATION_ERROR = 'sentence translation error occur'
    TRANSLATION_BAD_SERVER = 'service is not available'

    def __init__(self):
        pass

    def convert_between_ch_and_en_with_youdao(self, sentence, host_name='Talker', app_key='1797213575'):
        if sentence in (self.TRANSLATION_ERROR, self.TRANSLATION_BAD_SERVER):
            if self.convert_between_ch_and_en_with_youdao('Hi, how are you?') == self.TRANSLATION_ERROR:
                return self.TRANSLATION_BAD_SERVER
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

    def is_error_msg(self, msg):
        return msg in (self.TRANSLATION_ERROR, self.TRANSLATION_BAD_SERVER)


class SentenceTranslator(object):
    WAY_BAIDU = 'baidu'
    WAY_YOUDAO = 'youdao'

    def __init__(self, way=None):
        self.way = way or self.WAY_BAIDU
        if self.way == self.WAY_BAIDU:
            self.inst = SentenceTranslatorBaidu()
        elif self.way == self.WAY_YOUDAO:
            self.inst = SentenceTranslatorYouDao()
        else:
            self.inst = SentenceTranslatorBaidu()

    def convert_to_en(self, sentence):
        return self.inst.convert_to_en(sentence)

    def convert_to_cn(self, sentence):
        return self.inst.convert_to_cn(sentence)

    def is_error_msg(self, msg):
        return self.inst.is_error_msg(msg)

if __name__ == '__main__':
    t = SentenceTranslator()
    # msg = raw_input('input: ')
    print t.convert_to_en(u'你好吗？')

