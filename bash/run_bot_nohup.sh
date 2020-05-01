#!/usr/bin/env bash

cd ..

# python -m rasa_sdk.endpoint --actions actions

nohup rasa run --endpoints config/endpoints.yml --enable-api --m models --debug --cors "*" > logs/bot.log 2>&1 &