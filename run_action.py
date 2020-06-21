# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   run_action.py
 
@Time    :   2020/6/18 6:13 下午
 
@Desc    :
 
"""

#!/usr/bin/env python

# -*- coding: utf-8 -*-

from pudb import set_trace

set_trace()

def min(a,b):
    minValue = 0
    if(a >= b):
        minValue = b
    else:
        minValue = a
    return minValue

if __name__ == "__main__":
    a = 1
    b = 10
    minValue = 0
    while(a < b):
        minValue = min(a,b)

        print("minValue=",minValue)
        a += 1
        print("a=",a)