# -*- coding: utf-8 -*-

'''
@Author  :   Xu

@Software:   PyCharm

@File    :   actions.py

@Time    :   2019-09-10 16:31

@Desc    :   1、连接neo4j查询, 当rasa无法回复的时候到图数据库寻找答案
             2、重写name和run

             3、时间解析

'''

import pathlib
import os
import logging

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

from utils.time_utils import get_time_unit    # 时间解析

from py2neo import Graph, NodeMatcher


basedir = str(pathlib.Path(os.path.abspath(__file__)).parent.parent)

graph = Graph("http://172.18.103.43:7474")

selector = NodeMatcher(graph)

logger = logging.getLogger(__name__)

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

class ActionMyKB(ActionQueryKnowledgeBase):

    def __init__(self):
        knowledge_base = InMemoryKnowledgeBase(basedir + '/data/knowledge_base_data.json')
        knowledge_base.set_representation_function_of_object(
            "hotel", lambda obj: obj["name"] + " (" + obj["city"] + ")"
        )

        super().__init__(knowledge_base)

class ActionReportWeather(Action):
    '''
    天气查询
    '''
    def name(self) -> Text:
        return "action_report_weather"

    def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        address = tracker.get_slot('address')
        date_time = tracker.get_slot('date-time')

        if date_time is None:
            date_time = '今天'
        date_time_number = get_time_unit(date_time)  # 传入时间关键词，返回归一化的时间

        if isinstance(date_time_number, str):  # parse date_time failed
            return [SlotSet("matches", "暂不支持查询 {} 的天气".format([address, date_time_number]))]
        elif date_time_number is None:
            return [SlotSet("matches", "暂不支持查询 {} 的天气".format([address, date_time]))]
        else:
            print('address', address)
            print('date_time', date_time)
            print('date_time_number', date_time_number)
            weather_data = get_text_weather_date(address, date_time, date_time_number)    # 调用天气API
            return [SlotSet("matches", "{}".format(weather_data))]
