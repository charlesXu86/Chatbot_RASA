#!/usr/bin/env bash

cd ..
rasa train --domain domain/domain.yml --data data --config config/config_tf2.yml --out models