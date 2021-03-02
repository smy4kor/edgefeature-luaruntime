import time
import json
import os, sys

import urllib.request

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir + "/python-scripts")
print(parentdir)

from commands import DittoCommand
from dittoresponse import DittoResponse
from executor import LuaExecutor

# print(ScriptExecutor().executeAsLuaFile(currentdir + "/downloads/coffee-maker.lua"))
strRes = ScriptExecutor().executeAsLuaFile("/home/rollouts/git/edgefeature-luaruntime/demo-lua-scripts/show-current-time.lua")
print(strRes)

