#!/usr/bin/env bash

cd ..

python -m rasa_sdk.endpoint --actions actions

rasa run --endpoints config/endpoints.yml --enable-api --m models/20200103-163408.tar.gz --debug