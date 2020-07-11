#!/usr/bin/env bash


cd ..
rasa train --domain domain/domain.yml --data data --config config/config_with_components_tf1.yml --out models