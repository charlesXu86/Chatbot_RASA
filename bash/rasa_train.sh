#!/usr/bin/env bash


cd ..
rasa train --domain domain/domain_daogou.yml --data data --config config/config.yml --out models