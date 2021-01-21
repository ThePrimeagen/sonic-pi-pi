#!/usr/bin/env bash

source .env-export

# meant for local runs

if [[ "$PROD" -eq 1 ]]; then
    export SERVER=192.168.0.100
else
    export SERVER=0.0.0.0
fi

if [[ "$DEBUG" -eq 1 ]]; then
    python3 -m pudb.run client.py
else
    python3 client.py
fi


