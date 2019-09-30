# -*- coding: utf-8 -*-

'''
@Author  :   Xu

@Software:   PyCharm

@File    :   bot.py

@Time    :   2019-09-25 14:23

@Desc    :   可用于代码断点调试

'''

from rasa.core.channels.socketio import SocketIOInput
from rasa.core.agent import Agent
import rasa
from rasa.utils.endpoints import EndpointConfig


action_endpoint = EndpointConfig(url="http://localhost:5055")
# load your trained agent
agent = Agent.load('models',
                   action_endpoint=action_endpoint)
#
input_channel = SocketIOInput(
	# event name for messages sent from the user
	user_message_evt="user_uttered",
	# event name for messages sent from the bot
	bot_message_evt="bot_uttered",
	# socket.io namespace to use for the messages
	namespace=None
)


model = "models"
endpoints = "config/endpoints.yml"
credentials = "credentials.yml"
#
ss = rasa.run(model=model,
			  endpoints=endpoints,
			  credentials=credentials)