#!/usr/bin/env bash
# author: Xu

python -m rasa train core -c ../config/config.yml -s ../data/weather_stories.md --domain ../domain/weather_domain.yml --out ../models/  # --epochs 500 --nlu_threshold 0.4 --core_threshold 0.4