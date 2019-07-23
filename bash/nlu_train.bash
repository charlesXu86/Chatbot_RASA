#!/usr/bin/env bash
# author: bing

# python -m rasa train --config ../config/config.yml --data ../data/nlu_weather.json --path ../models --project Chatbot_Weather --fixed_model_name current -o models


#python -m rasa train nlu -c ../config/config_jieba_mitie_sklearn.json

python -m rasa train nlu --config ../config/config.yml --nlu ../data/nlu_weather.json --out ../models/nlu