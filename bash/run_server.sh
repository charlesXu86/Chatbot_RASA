#!/usr/bin/env bash


#python ../bot.py

#python -m rasa run actions ../actions.py # ../models/core-20190626-162009 -u default/current \
      # --port 5002 --credentials ../config/credentials.yml \
      # --cors * --endpoints ../config/endpoints.yml


python -m rasa run --endpoints config/endpoints.yml     \
                   --enable-api --m models  \
                   --port
                   --debug