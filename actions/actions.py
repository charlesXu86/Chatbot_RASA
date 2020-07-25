# -*- coding: utf-8 -*-

'''
@Author  :   Xu

@Software:   PyCharm

@File    :   actions.py

@Time    :   2019-09-10 16:31

@Desc    :   1、连接neo4j查询, 当rasa无法回复的时候到图数据库寻找答案
             2、重写name和run

             3、时间解析
             4、

'''

import pathlib
import os
import logging

from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker

from rasa_sdk.forms import FormAction, REQUESTED_SLOT

from service.weather_api.seniverse import SeniverseWeatherAPI
# from utils.time_utils import forecast_to_text

from service.FAQ import get_qa

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

logger = logging.getLogger(__name__)

basedir = str(pathlib.Path(os.path.abspath(__file__)).parent.parent)

api_secret = "Sq6NfAburbGs9MGQb"
sw = SeniverseWeatherAPI(api_secret)


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

    logger.info('Doing HeightWeightForm')
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
    '''
    天气查询
    '''

    def name(self) -> Text:
        return "action_report_weather"

    @staticmethod
    def required_slots(tracker):
        # type: () -> List[Text]
        """A list of required slots that the form has to fill"""
        return ["address", "date-time"]

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
            condition = sw.get_weather_by_city_and_day(address, date_time_number)  # 调用天气API
            weather_data = forecast_to_text(address, condition)

        return [SlotSet("matches", "{}".format(weather_data))]


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


class ActionUnknowIntent(Action):
    """
    处理未知意图，调用FAQ
    """
    def name(self):
        return 'action_unknow_intent'

    def run(selfs, dispatcher: CollectingDispatcher,
                   tracker: Tracker,
                   domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.latest_message.get('text')  # 用户说的话
        qa_message = get_qa(text)

        if qa_message != "未找到答案":
            dispatcher.utter_message("{}".format(qa_message))
        else:
            message = get_qa(text)
            if message['code'] == 100000 or message['code'] == 200000:
                dispatcher.utter_message("{}".format(message['text']))
            else:
                dispatcher.utter_template('utter_default', tracker, silent_fail=True)
        return []

class CaseForm(FormAction):
    """A custom form action"""

    def name(self):
        # type: () -> Text
        """Unique identifier of the form"""
        return "case_form"

    @staticmethod
    def required_slots(tracker):
        # type: () -> List[Text]
        """A list of required slots that the form has to fill"""
        return ["case", "place", "day"]

    def slot_mappings(self):
        return {"case": self.from_entity(entity="case", not_intent="unknown_intent"),
                "place": [self.from_entity(entity="place"),
                          self.from_text()],
                "day": [self.from_entity(entity="day"),
                        self.from_text()]
                }

    # # 无数据验证可省略
    # def validate(self,
    #              dispatcher: CollectingDispatcher,
    #              tracker: Tracker,
    #              domain: Dict[Text, Any]) -> List[Dict]:
    #     """Validate extracted requested slot
    #         else reject the execution of the form action
    #     """
    #     # extract other slots that were not requested
    #     # but set by corresponding entity
    #     slot_values = self.extract_other_slots(dispatcher, tracker, domain)
    #
    #     # extract requested slot
    #     slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
    #     if slot_to_fill:
    #         slot_values.update(self.extract_requested_slot(dispatcher,
    #                                                        tracker, domain))
    #         if not slot_values:
    #             # reject form action execution
    #             # if some slot was requested but nothing was extracted
    #             # it will allow other policies to predict another action
    #             raise ActionExecutionRejection(self.name(),
    #                                            "Failed to validate slot {0} "
    #                                            "with action {1}"
    #                                            "".format(slot_to_fill,
    #                                                      self.name()))
    #     return [SlotSet(slot, value) for slot, value in slot_values.items()]

    def submit(self, dispatcher, tracker, domain):
        # type: (CollectingDispatcher, Tracker, Dict[Text, Any]) -> List[Dict]
        """Define what the form has to do
            after all required slots are filled"""
        # utter submit template
        dispatcher.utter_template('utter_search_template', tracker)
        dispatcher.utter_message("{},在{}发生一起性质恶劣的{},引起全市人民的高度关注，以下是详细信息："
                                 .format(tracker.get_slot("day"), tracker.get_slot("place"), tracker.get_slot("case")))
        return [AllSlotsReset()]



