import time
import json
import os, sys

import urllib.request

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir + "/python-scripts")

from commands import DittoCommand
from dittoresponse import DittoResponse
from agent import Agent
from softwareFeatureCache import SoftwareFeatureCache

# agent = Agent("sandeep agent","2.0.0","sanagent","some-feature-id")
res = SoftwareFeatureCache.loadOrCreate('sandeep')
res.save()
