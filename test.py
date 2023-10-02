import requests
import json
import time
import random
import os


localDirectory = os.path.dirname(os.path.abspath(__file__))
file = "trafficPeakparams.json"
fileWithPath = (f"{localDirectory}/{file}")
f = open(fileWithPath, "r")  # Read the doc from a file
trafficPeak = json.loads(f.read(-1))
print(trafficPeak)
print("url :"+trafficPeak["ingestURL"])
print("username :"+trafficPeak["username"])
print("password :"+trafficPeak["password"])
