# -*- coding: UTF-8 -*-

"""
Desc: django util.
Note:

---------------------------------------
# 2016/05/22   kangtian         created
"""

import time
import json
import random
import traceback

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

cookie = {
    'remember_user_token': 'W1sxNzYwOTgyXSwiJDJhJDEwJGhabE5kM1V6YW8xcG5iVXdPeUhOb08iLCIxNDYzMzI3OTE0LjU3OTYyNDciXQ',
    'read_mode': 'night',
    'locale': 'zh-CN',
    'default_font': 'font2',
    # 'Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068': '1463917670',
    # 'Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068': '1463285905%2C1463905082%2C1463909186%2C1463912476',
    # '__utma': '194070582.1342553755.1463918997.1463918997.1463918997.1',
    # '__utmb': '194070582.7.10.1463918997',
    # '__utmc': '194070582',
    # '__utmt': '1',
    # '__utmv': '194070582.|2=User%20Type=Member=1',
    # '__utmz': '194070582.1463918997.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    # '_session_id': 'MFd2ZE93ZHg1QkErTkVzNWFtOU81NHMrVkJ1V0N4YUNicUxLWnQwaWdjUmczMzBweTRibDRodXJmUk5telNXZExJRzhBbjNBN0tsSVJTV0xORUdmTHBDQmRrSG5mcUF2MEY3UXFSUEVmVk51QWM1S0NIbGRZc0ZxUjZEY0dIRFplWE9ObGpWS2d4ZHpwZHhPamp5Q2JYZWFWUVBsVkxXOERFK3BlL1QrRE8yK0RDYWVwd3BZNHVYQ2Q1VkNObUpiK2l0TkhpZzQ2TVJBVGZNaVExWkxMcHl0WjBjYnZxSER3ZmVLMko3aUVUTUVSVXBGWlIzMzFBUkYydlhHRXdhaEtmMU9nOE5zcGlBMzZxUk94NkplaFRsdUNWNW9OT1IrZWpDM1JUNGkxbVp3VDNneVRTNFo1U3hKK1RoU2tkYWZ0M3FNb1FBY2hXUFNwSmkzYytqMm5tenEyVzBXTThFdHg1cU0xNWFSV2JMTjBnRFBUL1FGOCtlTFdRbjNOUXlDSCtUMlIvOUlTMHl4cEl2WDRYSTNCRjgxbVp3NTZERmtSN1l1WmtqTkRCY3JmVjcyaUN5VWlicC9QRWQyWGpDVHpSNVB1UkM2Y25WL0dmRkFHbDV0VTFSZUFFWVIwQTdsQndCb21FaWlZK3M9LS1Pei9IdXJtZ0JhLzFqRXRtdkYrU3dBPT0',
}


class BrowserBase(object):
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.win_name_dict = dict()

    @property
    def inst(self):
        return self.browser

    def add_cookie_with_kv_dict(self, kv_dict):
        for k, v in kv_dict.iteritems():
            self.browser.add_cookie({'name': k, 'value': v})

    def open_url(self, url):
        self.browser.get(url)

    def wait(self, timeout_sec):
        WebDriverWait(self.inst, timeout_sec)

    def switch_to_window(self, window_name):
        self.inst.switch_to.window(window_name)

    def get_window_name(self):
        print '======'
        for window in self.inst.window_handles:
            print window
        current = self.inst.current_window_handle

    def set_nick_of_unnamed_window(self, nick):
        for window in self.inst.window_handles:
            window_name = str(window)
            if window_name not in self.win_name_dict:
                self.win_name_dict[window_name] = nick
            print window

    def get_window_list_width_nick(self, nick):
        window_list = list()
        for window_name, nick_name in self.win_name_dict.iteritems():
            if nick == nick_name:
                window_list.append(window_name)
        return window_list

    def switch_to_nick(self, nick):
        window_list = self.get_window_list_width_nick(nick)
        window_name = ''
        if window_list:
            window_name = window_list[0]
            self.switch_to_window(window_name)
        return window_name

    def print_nick_mapping(self):
        print json.dumps(self.win_name_dict, indent=4)

    def close_window(self, closed_name, open_name):
        # self.inst.close()
        self.switch_to_window(open_name)

    def switch_to_new_tab(self, name):
        self.set_nick_of_unnamed_window(name)
        window_names = self.get_window_list_width_nick(name)
        if window_names:
            window_name = window_names[0]
            self.switch_to_window(window_name)
            return window_name
        return ''


class WebPageAuto(BrowserBase):
    def __init__(self):
        super(WebPageAuto, self).__init__()

    def quit(self):
        self.inst.quit()


class JinShuAuto(WebPageAuto):
    def __init__(self):
        super(JinShuAuto, self).__init__()
        self.d = dict()
        self.main_name = 'main'

    def login(self):
        login_elem = self.inst.find_element_by_link_text(u'登录')
        login_elem.click()
        sign_in_name = self.inst.find_element_by_id('sign_in_name')
        sign_in_name.click()
        sign_in_name.send_keys('18874293064')
        sign_in_password = self.inst.find_element_by_id('sign_in_password')
        sign_in_password.click()
        sign_in_password.send_keys('tiankang')
        raw_input("Login, Enter ~~~")
        submit_btn = self.inst.find_element_by_css_selector('.submit-button')
        submit_btn.click()

    def load_more(self, page_num=15):
        for i in range(page_num):
            try:
                more_elem = self.inst.find_element_by_class_name('ladda-button')
                if not more_elem:
                    continue
                more_elem.click()
                time.sleep(1)
            except:
                continue

    def start(self):
        entry_url = 'http://www.jianshu.com/'
        self.open_url(entry_url)
        assert u'首页 - 简书' in self.inst.title

        self.set_nick_of_unnamed_window(self.main_name)
        self.add_cookie_with_kv_dict(cookie)

        self.login()

        # click newer
        newer = self.inst.find_element_by_link_text(u'新上榜')
        newer.click()
        self.load_more(page_num=20)

        time.sleep(1)

        author_list = self.inst.find_elements_by_class_name('author-name')
        for index in range(len(author_list[:10])):
            self.switch_to_nick(self.main_name)
            author_list = self.inst.find_elements_by_class_name('author-name')
            try:
                self.handle_author(author_list[index])
            except:
                print traceback.format_exc()

    def handle_author(self, author_elem):
        author_name = author_elem.text
        author_elem.click()
        time.sleep(1)

        author_nick = author_name + u' - 简书'
        self.set_nick_of_unnamed_window(author_nick)
        if not self.switch_to_nick(author_nick):
            raise Exception('switch_to_nick failed')
        self.print_nick_mapping()
        follow = self.inst.find_element_by_css_selector('.follow a')
        if follow.text == u'添加关注':
            follow.click()
        else:
            return None

        self.inst.find_element_by_css_selector('.basic-info .btn-group .btn-list').click()
        write_letter = self.inst.find_element_by_css_selector('.basic-info .btn-group .dropdown-menu :first-child')
        write_letter.click()
        time.sleep(1)
        # letter_nick = author_name + u' - 简信'
        # self.set_nick_of_unnamed_window(letter_nick)
        # self.switch_to_nick(letter_nick)
        input_elem = self.inst.find_element_by_id('chat_message_content')
        print 'input_elem: %s' % input_elem.text
        input_elem.click()
        input_elem.send_keys(self.gen_hello())
        submit_elem = self.inst.find_element_by_name('commit')
        submit_elem.click()

    def gen_hello(self):
        list_1 = [u'众里寻你千百度，已关注', u'已关注亲了', u'关注亲了哦', u'偶已关注', u'今天是个好天气，好呀好天气，已关注']
        list_2 = [u'，求互粉', u'，求大大互粉 ', u'，跪求互粉', u'，跪求互粉一把']
        list_3 = [u'  ≧◇≦', u' ~^o^~', u' ↖(^0^)↗', u' (×_×)', u' 共同进步哈 :)']
        hello = random.choice(list_1) + random.choice(list_2) + random.choice(list_3)
        print 'gen_hello: %s' % hello
        return hello


def run():
    w = JinShuAuto()
    w.start()
    # raw_input("Enter to quit ~~~")

    print 'END ~~'
    time.sleep(100)
    w.quit()

run()
