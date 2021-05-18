#!/usr/bin/env bash

VENVNAME=ass1

python3 -m venv $VENVNAME
source $VENVNAME/bin/activate

pip --version
pip install --upgrade pip
test -f requirements.txt && pip install -r requirements.txt

echo "build $VENVNAME"