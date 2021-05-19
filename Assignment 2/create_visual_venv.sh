#!/usr/bin/env bash

VENVNAME=ass2

python3 -m venv $VENVNAME
source $VENVNAME/bin/activate

pip --version
pip install --upgrade pip

test -f requirements.txt && pip install -r requirements.txt

# build output folder
mkdir -p A2_output/

echo "build $VENVNAME"
