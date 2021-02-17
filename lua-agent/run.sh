#!/usr/bin/env bash

echo "Creating a SoftwareUpdatable agent of type lua"
python /python-scripts/register-agent.py

echo "Subscribing for mqtt announcements"
## python /python-scripts/subscribe-for-commands.py