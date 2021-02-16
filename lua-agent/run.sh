#!/usr/bin/env bash

echo "Creating a SoftwareUpdatable agent of type lua"
python register-agent.py

echo "Subscribing for mqtt announcements"
## python subscribe.py