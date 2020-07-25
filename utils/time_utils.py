# -*- coding: utf-8 -*-

"""
@Author  :   Xu

@Software:   PyCharm

@File    :   time_utils.py

@Time    :   2020-01-15 10:53

@Desc    :   时间解析，这里调用time_convert包

            pip install time_convert

"""
import datetime
import logging

from time_convert import TimeNormalizer

logger = logging.getLogger(__name__)

tc = TimeNormalizer()


def get_time_unit(msg):
    '''
    传入对话，返回日期
    :param msg:
    :return:
    '''

    res = tc.parse(msg)
    date_unit = res['date'][:10]
    data = datetime.datetime.strptime(date_unit, '%Y-%m-%d').date()
    return data

def forecast_to_text(address, condition):
    msg_tpl = "{city} {date} 的天气情况为：{condition}；气温：{temp_low}-{temp_high} 度"
    msg = msg_tpl.format(
        city= address,
        date=condition.date,
        condition=condition.condition,
        temp_low=condition.low_temperature,
        temp_high=condition.high_temperature
    )
    return msg


if __name__ == '__main__':
    msg = '明天上午，沈海高速全线封停'
    get_time_unit(msg)
