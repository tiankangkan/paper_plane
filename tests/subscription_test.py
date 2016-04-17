# -*- coding: utf-8 -*-

import paper_plane.django_init
from paper_plane.url_manager import UrlManager
from k_util.http_util import post_request


def request_with_text_msg():
    url = UrlManager().get_url_of_weixin_entry()
    xml_str = u"""
        <xml>
        <ToUserName><![CDATA[oA1YQwEJImFeINpTvBI160n6Eu2Q]]></ToUserName>
        <FromUserName><![CDATA[gh_d9b64eb9e787]]></FromUserName>
        <CreateTime>1460873374</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[ baby ]]></Content>
        </xml>
    """
    resp = post_request(url, data=xml_str)
    print resp


if __name__ == '__main__':
    request_with_text_msg()
