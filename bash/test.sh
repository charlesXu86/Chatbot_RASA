#!/usr/bin/env bash

cd "$(dirname $0)"
project=$(pwd | cut -d / -f 5)
echo 'project: '$project

CURDIR=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )

echo $CURDIR


echo $(dirname $(pwd))