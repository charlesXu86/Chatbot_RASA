#!/usr/bin/env bash


cd ..
rasa train --domain domain/domain.yml --data data --config config/config.yml --out models