#!/usr/bin/env bash


python ../server.py

python -m rasa run actions ../actions.py # ../models/core-20190626-162009 -u default/current \
      # --port 5002 --credentials ../config/credentials.yml \
      # --cors * --endpoints ../config/endpoints.yml