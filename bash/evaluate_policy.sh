#!/usr/bin/env bash

python -m rasa train compare -c policy_config1.yml policy_config2.yml -d domain.yml -s stories_folder -o comparison_models --runs 3 --percentages 0 5 25 50 70 90 95


