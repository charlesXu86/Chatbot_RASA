# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   time_utils.py
 
@Time    :   2020-01-15 10:53
 
@Desc    :   时间解析，这里调用time_convert包
 
'''

import time_convert as tv

from time_convert import TimeNormalizer

tc = TimeNormalizer()

def get_time_unit(msg):
    '''
    传入对话，返回日期
    :param msg:
    :return:
    '''

    res = tc.parse(msg)

    return res