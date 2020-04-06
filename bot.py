# -*- coding: utf-8 -*-

'''
@Author  :   Xu

@Software:   PyCharm

@File    :   bot.py

@Time    :   2019-09-25 14:23

@Desc    :   可用于代码断点调试

'''

import rasa
import pathlib
import os

basedir = str(pathlib.Path(os.path.abspath(__file__)).parent)
model = basedir + "/models"


endpoints = "config/endpoints.yml"
credentials = "config/credentials.yml"
#
ss = rasa.run(model=model,
			  endpoints=endpoints,
			  credentials=credentials
			  )