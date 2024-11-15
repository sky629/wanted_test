#!/bin/bash

env_name="venv"
python3 -m venv $env_name
source $env_name/bin/activate

if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "venv activated: $VIRTUAL_ENV"
else
    echo "venv fail."
fi

pip install --upgrade pip
pip install -r req.txt