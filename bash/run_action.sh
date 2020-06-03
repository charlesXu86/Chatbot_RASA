#!/usr/bin/env bash

cd ..
nohup python -m rasa_sdk.endpoint --actions actions > $(dirname $(pwd))/Chatbot_RASA/logs/action.log 2>&1 &