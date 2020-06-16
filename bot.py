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

from rasa.core.agent import Agent
from rasa.core import config

basedir = str(pathlib.Path(os.path.abspath(__file__)).parent)
model = basedir + "/models"

endpoints = "config/endpoints.yml"
credentials = "credentials.yml"
#
ss = rasa.run(model=model,
              endpoints=endpoints,
              credentials=credentials
              )


def train_dialogue_transformer(domain_file="mobile_domain.yml",
                               model_path="models/dialogue_transformer",
                               training_data_file="data/mobile_edit_story.md"):
    # 通过加载yml配置文件方式配置policy
    policies = config.load('./policy/attention_policy.yml')
    agent = Agent(domain_file,
                  policies=policies)

    training_data = agent.load_data(training_data_file)
    agent.train(
        training_data,
        validation_split=0.2
    )

    agent.persist(model_path)
    return agent
