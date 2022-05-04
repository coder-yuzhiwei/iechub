# 访问图灵机器人openapi
# -*- coding: utf-8 -*-
"""
    ChatApis.py
    ~~~~~~~~~

    图灵机器人(公司)闲聊系统API对接
    免费版只限每天调用100次，需联外网

    :date: 2020-02-10 15:56:00
    :author: by jiangdg
"""
from urllib.parse import urlencode

import requests
import json


def get_response(msg):
    """
        访问图灵机器人openApi

        :param msg 用户输入的文本消息
        :return string or None
    """
    apiurl = "http://api.qingyunke.com/api.php"
    # 构造请求参数实体
    params = {"key": 'free',
              "appid": 0,
              "msg": msg,
              }
    # 将表单转换为json格式
    print(params)
    content = urlencode(params)
    print(content)
    apiurl = apiurl + '?' +content
    # 发起post请求
    r = requests.get(url=apiurl, verify=False).json()
    print("r = " + str(r))
    return r['content']

if __name__ == '__main__':
    r = get_response("武汉天气怎么样")
    print(r)