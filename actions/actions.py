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
import requests

from typing import Any, Text, Dict, List, Union

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
from rasa_sdk.forms import FormAction
from rasa_sdk.knowledge_base.storage import KnowledgeBase

from utils.time_utils import get_time_unit  # 时间解析
# from aip.HeWeather import get_weather

from service.action import get_text_weather_date
from service.normalization import text_to_date
from service.weather_api import get_weather_api



# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

basedir = str(pathlib.Path(os.path.abspath(__file__)).parent.parent)


def get_tuling_response(msg):
    # 替换成自己的key
    key = "xxx"
    api = 'http://www.tuling123.com/openapi/api?key={}&info={}'.format(
        key, msg)
    return requests.get(api).json()


class ActionAskProblem(Action):
    '''
    询问问题
    '''

    def name(self) -> Text:
        return "action_ask_problem"

    def run(self,
            dispatcher: CollectingDispatcher,  # Send messages back to user
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # KB-QA
        txt = tracker.latest_message['text']  # 最新一轮对话的text，作为query传入知识库查询
        # car = tracker.get_slot('car')
        # result = list(selector.match())   # 这里查询neo4j

        print(txt)
        result = ''

        dispatcher.utter_message('这里查询知识库')
        return [SlotSet('org', result if result is not None else [])]


class ActionDefaultFallback2(Action):
    '''
    默认回复
    '''

    def name(self):  # type: () -> Text
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


class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "my_fallback_action"

    def run(self, dispatcher, tracker, domain):
        # dispatcher.utter_template("utter_my_default", tracker)
        state = tracker.current_state()
        logger.info("action_my_fallback_action current state is {}\n".format(state))
        message_text = tracker.latest_message.get('text')
        response = get_tuling_response(message_text).get('text')
        logger.info("action_my_fallback_action latest_message is {},response is {}".format(message_text, response))
        dispatcher.utter_message(response)
        # return [UserUtteranceReverted()]
        return []


class HeightWeightForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "height_weight_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["height", "weight"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "height": [
                self.from_entity(
                    entity="height", intent=["inform_height_weight"]
                ),
            ],
            "weight": [
                self.from_entity(
                    entity="weight", intent=["inform_height_weight"]
                ),
            ],
        }

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        # print("submit------tracker is {}",tracker)
        slot_to_fill = tracker.get_slot("requested_slot")
        logger.info("-------submit start slot_to_fill is '{}'"
                    "".format(slot_to_fill))
        # utter submit template
        dispatcher.utter_template("utter_cloth_recommend", tracker)
        return []


class ActionMyKB(ActionQueryKnowledgeBase):

    def __init__(self):
        knowledge_base = InMemoryKnowledgeBase(basedir + '/data/knowledge_base_data.json')
        knowledge_base.set_representation_function_of_object(
            "hotel", lambda obj: obj["name"] + " (" + obj["city"] + ")"
        )

        super().__init__(knowledge_base)


class ActionReportWeather(Action):
    def __init__(self):
        self.weather_api = get_weather_api('seniverse')
    logger.info('Do ActionReportWeather')

    def name(self) -> Text:
        return "action_report_weather"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        address = tracker.get_slot('address')
        logger.info('Slot Address {}'.format(address))
        date_time = tracker.get_slot('date-time')
        logger.info('Slot Date_time {}'.format(date_time))
        if date_time is None:
            msg = "暂不支持查询 {} 的天气".format([address, date_time])
            return [SlotSet("matches", msg)]

        else:
            try:
                date_object = get_time_unit(date_time)
                weather_data = self.weather_api.get_text_by_city_and_day(address, date_object)
            except Exception as e:
                weather_data = str(e)

            return [SlotSet("matches", "{}".format(weather_data))]