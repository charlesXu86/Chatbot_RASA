# -*- coding: utf-8 -*-

'''
@Author  :   Xu

@Software:   PyCharm

@File    :   actions.py

@Time    :   2019-09-10 16:31

@Desc    :   1、连接neo4j查询, 当rasa无法回复的时候到图数据库寻找答案
             2、重写name和run

'''

import requests
import json

from typing import Any, Text, Dict, List

from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker
from py2neo import Graph, NodeMatcher


graph = Graph("http://172.18.103.43:7474")

selector = NodeMatcher(graph)


class ActionAskProblem(Action):
    '''
    询问问题
    '''
    def name(self) -> Text:
        return "action_ask_problem"

    def run(self,
            dispatcher: CollectingDispatcher,   # Send messages back to user
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # KB-QA
        # car = tracker.get_slot('car')
        # result = list(selector.match())   # 这里查询neo4j
        result = ''

        dispatcher.utter_message('这里查询知识库')
        return [SlotSet('org', result if result is not None else [])]

class ActionDefaultFallback(Action):
    '''
    默认回复
    '''
    def name(self): # type: () -> Text
        return "action_default_fallback"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]

        result = ''
        dispatcher.utter_message("我不知道您在说什么哟，请换一种方式吧")
        return [SlotSet('org', result if result is not None else [])]