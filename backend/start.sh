#!/usr/bin/env bash

nohup ngrok start --all > /home/mu/temp/ngrok.log 2>&1 &
exec python3 `dirname $0`/line.py
