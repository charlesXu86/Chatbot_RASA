#!/usr/bin/env bash


cd ..
rasa train --domain domain/cuishou_domain.yml --data data --config config/config_with_components.yml --out models