#!/bin/bash
if [[ "$VIRTUAL_ENV" != "" ]]; then
    pip install -r requirements.txt
else
    echo "Error: Please run this script in a Python 3 virtualenv"
    exit 1;
fi
