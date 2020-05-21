#!/usr/bin/env bash

cd ..
rasa run --endpoints config/endpoints.yml --enable-api --m models --log-file $(dirname $(pwd))/Chatbot_RASA/logs/bot.log --debug --cors "*"

# rasa run -m models --enable-api --log-file out.log -p 5500 --cors "*"