
import requests
import json
import time
import random
import os
import urllib
import logging
from urllib.parse import urlparse

# Trying for bulk request


def sendDataToTrafficPeak(url, username, password, count, jsonData):
    """This function will send data to TrafficPeak:
    url: The URL for the data ingest endpoint. 
    username: The username for data ingest endpoint
    password: The password for the data ingest endpoint
    count: how many records to send
    jsonData: A json object outlining the type of log data to send to simulate DS2 data. (URL,country,response code etc)
    """
    headers = {"Content-type": "application/json"}
    auth = (username, password)
    # This is where we will store the large file we're creating with 'count' request records
    bulkFile = open("bulkFile.txt", "w")
    # File will represent log lines as an array of JSON objects. This opens the array.
    bulkFile.write("[\n")

    # print(f"Count is: {count}")
    for x in range(int(count)):
        # print(f"x is {x}")
        jsonObj = json.loads(jsonData)  # Turns file json into object
        # By default, these requests will use random timestamps over the past 24 hours
        jsonObj["reqTimeSec"] = int(time.time()-random.randrange(1, 60*60*24))

        for key in jsonObj:  # Loop through all elements of send data
            # If list of values is provided, randomly pick one
            if type(jsonObj[key]) == list:
                jsonObj[key] = jsonObj[key][random.randint(
                    0, len(jsonObj[key])-1)]
        # bulkFile.write("{ \"create\" : { \"_index\" : \"datastream2\"} }\n")
        if x > 0:
            # put a comma in front of each entry except the first
            bulkFile.write(",")
        bulkFile.write(json.dumps(jsonObj))

    # Chop off the last comma in the file, then close the array in the file

    bulkFile.write("]")
    bulkFile.close()

    # Trying for bulk request
    f = open("bulkFile.txt", "r")

    # Send the data to TrafficPeak and get response:
    sendBody = f.read(-1)
    r = requests.post(url, data=sendBody, headers=headers, auth=auth)
    return r.text


localDirectory = os.path.dirname(os.path.abspath(__file__))
file = "trafficPeakparams.json"
fileWithPath = (f"{localDirectory}/{file}")
f = open(fileWithPath, "r")  # Read the doc from a file
trafficPeak = json.loads(f.read(-1))

# Send general data. Several file types, mostly 200 responses
#
localDirectory = os.path.dirname(os.path.abspath(__file__))
file = "ds2TemplateGeneralData.json"
fileWithPath = (f"{localDirectory}/{file}")
f = open(fileWithPath, "r")  # Read the doc from a file
myJsonData = f.read(-1)  # Read the entire file into sendBody variable
myJsonData = myJsonData.replace("\n", "")  # Strip any newlines
print("\n******** JSON Data:\n")
print(myJsonData)
print("\n********\n")

myResponse = sendDataToTrafficPeak(
    trafficPeak["ingestURL"], trafficPeak["username"], trafficPeak["password"], 10000, myJsonData)
print("\n****RESPONSE: \n")
print(myResponse)
f.close

# Send data for some large files
file = "ds2TemplateLargeFiles.json"
fileWithPath = (f"{localDirectory}/{file}")
f = open(fileWithPath, "r")  # Read the doc from a file
myJsonData = f.read(-1)  # Read the entire file into sendBody variable
myJsonData = myJsonData.replace("\n", "")  # Strip any newlines
print("\n***JSON DATA2\n")
print(myJsonData)
print("\n***RESPONSE 2\n")
myResponse = sendDataToTrafficPeak(
    trafficPeak["ingestURL"], trafficPeak["username"], trafficPeak["password"], 10000, myJsonData)
print(myResponse)
print("\n********\n")

# Next, send some sample requests with errors 401,403,302 etc
file = "ds2TemplateErrorRequests.json"
fileWithPath = (f"{localDirectory}/{file}")
f = open(fileWithPath, "r")  # Read the doc from a file
myJsonData = f.read(-1)  # Read the entire file into sendBody variable
myJsonData = myJsonData.replace("\n", "")  # Strip any newlines
print("\n***JSON DATA2\n")
print(myJsonData)
print("\n***RESPONSE 2\n")
myResponse = sendDataToTrafficPeak(
    trafficPeak["ingestURL"], trafficPeak["username"], trafficPeak["password"], 1000, myJsonData)
print(myResponse)
print("\n********\n")
f.close
