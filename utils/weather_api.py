# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   weather_api.py
 
@Time    :   2019-10-09 16:45
 
@Desc    :
 
'''

import requests

def get_response(msg):
    key = ' '
    api = 'http://www.tuling123.com/openapi/api?key={}&info={}'.format(
        key, msg)
    return requests.get(api).json()