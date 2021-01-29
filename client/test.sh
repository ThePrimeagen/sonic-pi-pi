#!/usr/bin/env bash

source .env-export

# meant for local runs

if [[ "$PROD" -eq 1 ]]; then
    export MUSIC_SERVER=192.168.0.100:42069
    export UI_SERVER=0.0.0.0:6969
else
    export MUSIC_SERVER=0.0.0.0:42069
    export UI_SERVER=0.0.0.0:6969
fi

if [[ "$DEBUG" -eq 1 ]]; then
    python3 -m pudb.run client.py
else
    python3 client.py
fi


