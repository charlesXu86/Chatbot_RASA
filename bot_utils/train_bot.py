# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   train_bot.py
 
@Time    :   2020/7/16 11:19 下午
 
@Desc    :   请求前端接口，查询数据、组装数据，训练模型
             1、domain
             2、config
             3、nlu
             4、stories
             5、force
             6、save_to_default_model_directory
 
"""

from utils.mysql_utils import SkillData

# class TrainBot():
#
#     def __init__(self):
#         self.db  = SkillData().get_data()

skillId = '123445'

all_data = SkillData().get_data(skillId=skillId)

