#!/usr/bin/env bash

cd ..

python -m rasa_sdk.endpoint --actions actions

rasa run --endpoints config/endpoints.yml --enable-api --m models/20191106-105047.tar.gz --debug