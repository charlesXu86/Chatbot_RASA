#!/usr/bin/env bash

cd ..
rasa run --endpoints config/endpoints.yml --enable-api --m models/20191004-145426.tar.gz --debug