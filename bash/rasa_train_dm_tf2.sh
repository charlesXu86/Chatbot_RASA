#!/usr/bin/env bash

cd ..
rasa train --domain domain/domain.yml --data data --out models core --config config/config_tf2.yml

rasa train --domain domain.yml --data data --out models core --config config/config_tf2.yml