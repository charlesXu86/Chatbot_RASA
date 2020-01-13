#!/usr/bin/env bash

cd ..
nohup python -m rasa_sdk.endpoint --actions actions > action.log 2>&1 &