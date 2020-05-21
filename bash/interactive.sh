#!/usr/bin/env bash

cd ..
#rasa interactive -m models --endpoints config/endpoints.yml \
#                           --debug-plots True
#                           --skip-visualization True

rasa interactive -m models --config config/config.yml