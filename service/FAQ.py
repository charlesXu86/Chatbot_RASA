# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   FAQ.py
 
@Time    :   2020/6/13 11:18 上午
 
@Desc    :   调用FAQ引擎
 
"""

import json
import logging

import requests

logger = logging.getLogger(__name__)


def get_qa(msg):
    """

    :param msg:
    :return:
    """

    url = 'http://172.18.86.20:9008/api/qa'
    data = {
        "msg": msg
    }
    post_data = json.dumps(data)
    response = requests.post(url=url, data=post_data)
    logger.info('statusCode is {}'.format(response.status_code))

    if response.status_code == 200:
        anwser = json.loads(list({response.text})[0])['result']['anwser']
    else:
        anwser = '没有答案'

    return anwser

if __name__ == '__main__':
    msg = '一万'
    get_qa(msg)