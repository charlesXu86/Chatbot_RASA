# -*- coding: utf-8 -*-

'''
@Author  :   Xu

@Software:   PyCharm

@File    :   actions.py

@Time    :   2019-09-10 16:31

@Desc    :   1、连接neo4j查询, 当rasa无法回复的时候到图数据库寻找答案
             2、重写name和run

'''

import pathlib
import os

from typing import Any, Text, Dict, List

from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker

from rasa_sdk.knowledge_base.utils import (
    SLOT_OBJECT_TYPE,
    SLOT_LAST_OBJECT_TYPE,
    SLOT_ATTRIBUTE,
    reset_attribute_slots,
    SLOT_MENTION,
    SLOT_LAST_OBJECT,
    SLOT_LISTED_OBJECTS,
    get_object_name,
    get_attribute_slots,
)

from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.storage import KnowledgeBase

from py2neo import Graph, NodeMatcher


basedir = str(pathlib.Path(os.path.abspath(__file__)).parent.parent)

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
        txt = tracker.latest_message['text']     # 最新一轮对话的text，作为query传入知识库查询
        # car = tracker.get_slot('car')
        # result = list(selector.match())   # 这里查询neo4j

        print(txt)
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

# class ActionAskWeather(Action):
#     '''
#     天气查询
#     '''
#     pass


class ActionMyKB(ActionQueryKnowledgeBase):

    def __init__(self):
        knowledge_base = InMemoryKnowledgeBase(basedir + '/data/knowledge_base_data.json')
        knowledge_base.set_representation_function_of_object(
            "hotel", lambda obj: obj["name"] + " (" + obj["city"] + ")"
        )

        super().__init__(knowledge_base)