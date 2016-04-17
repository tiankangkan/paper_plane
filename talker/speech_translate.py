# -*- coding: UTF-8 -*-

"""
Desc: translate speech.
Note:

---------------------------------------
# 2016/04/07   kangtian         created

"""

import json
import urllib2, urllib
import base64

from k_util.str_op import to_utf_8


class SpeechTranslate(object):
    TRANSLATION_ERROR = 'speech translation error occur'
    TRANSLATION_NOT_MATCH = 'speech translation not match'

    def __init__(self):
        self.server_audio2text = 'http://vop.baidu.com/server_api'
        self.server_text2audio = 'http://tsn.baidu.com/text2audio'
        self.token = ''
        self.api_key = 'MXecjVUFiHXE5yhHpKioqsIz'
        self.secretKey = '90158e69bd83a6d2dbf0d90854616796'
        self.cuid = '8004536'

    def get_token(self):
        get_token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials" + "&client_id=" + \
                        self.api_key + "&client_secret=" + self.secretKey
        req = urllib2.Request(get_token_url)
        resp_str = urllib2.urlopen(req).read()
        resp = json.loads(resp_str)
        self.token = resp['access_token']

    def check_token(self):
        if not self.token:
            self.get_token()

    def get_text_of_speech(self, file_path):
        file_data = ''
        with open(file_path, 'rb') as fp:
            while True:
                read_data = fp.read()
                if read_data:
                    file_data += read_data
                else:
                    break
        file_len = len(file_data)
        self.check_token()
        post_data = dict(
            format='wav',
            rate=16000,
            channel='1',
            token=self.token,
            cuid=self.cuid,
            len=file_len,
            speech=base64.b64encode(file_data)
        )
        req = urllib2.Request(self.server_audio2text, data=json.dumps(post_data), headers={'Content-type': 'text/json'})
        resp_str = urllib2.urlopen(req).read()
        resp = json.loads(resp_str)
        text = self.TRANSLATION_ERROR
        if resp['err_no'] == 0:
            text_list = resp['result']
            text = text_list[0] if text_list else self.TRANSLATION_ERROR
        elif resp['err_no'] == 3301:
            text = self.TRANSLATION_NOT_MATCH
        return text

    def get_speech_of_text(self, text, to_file=None, speech_sex='woman'):
        self.check_token()
        per = 0 if speech_sex == 'woman' else 1
        post_data = dict(
            tok=self.token,
            cuid=self.cuid,
            lan='zh',
            ctp=1,
            spd=6,
            pit=5,
            vol=5,
            per=per,
        )
        post_data['tex'] = to_utf_8(text)    # not support unicode
        data = urllib.urlencode(post_data)
        # print self.server_text2audio+'?'+data
        req = urllib2.Request(self.server_text2audio, data=data)
        resp = urllib2.urlopen(req).read()
        if resp[0] == '{':
            print 'Error: %s' % resp
        else:
            if to_file:
                with open(to_file, 'wb') as fp:
                    fp.write(resp)
        return resp


SPEECH_TRANSLATE = SpeechTranslate()


if __name__ == '__main__':
    s = SpeechTranslate()
    s.get_token()
    s.get_speech_of_text(text='啊哈。', to_file='test.mp3')
    # print s.get_text_of_speech('/Users/kangtian/Documents/Master/talker/talker/record_2016_04_15__01_35_12_918743.wav')
    # s.play_wava('/Users/kangtian/Documents/Master/talker/record_1.wav')
    # s.record_wava('/Users/kangtian/Documents/Master/talker/record_2.wav')

