
import requests
import json
import time
import random
import os
import urllib
import logging
from urllib.parse import urlparse

# Trying for bulk request


def sendDataToTrafficPeak(templateFileName, count):
    """This function will send data to TrafficPeak:
    url: The URL for the data ingest endpoint. 
    username: The username for data ingest endpoint
    password: The password for the data ingest endpoint
    count: how many records to send
    jsonData: A json object outlining the type of log data to send to simulate DS2 data. (URL,country,response code etc)
    """

    # Read the URL, username and password from the local file trafficPeakparams.json
    localDirectory = os.path.dirname(os.path.abspath(__file__))
    file = "trafficPeakparams.json"
    fileWithPath = (f"{localDirectory}/{file}")
    f = open(fileWithPath, "r")  # Read the doc from a file
    trafficPeak = json.loads(f.read(-1))
    f.close

    # Read the template file into a JSON string
    localDirectory = os.path.dirname(os.path.abspath(__file__))
    fileWithPath = (f"{localDirectory}/{templateFileName}")
    f = open(fileWithPath, "r")  # Read the doc from a file
    jsonData = f.read(-1)  # Read the entire file into sendBody variable
    jsonData = jsonData.replace("\n", "")  # Strip any newlines
    f.close

    # prepare the file which will have all the log lines
    headers = {"Content-type": "application/json"}
    auth = (trafficPeak["username"], trafficPeak["password"])
    # This is where we will store the large file we're creating with 'count' request records
    bulkFile = open("bulkFile.txt", "w")
    # File will represent log lines as an array of JSON objects. This opens the array.
    bulkFile.write("[\n")

    # print(f"Count is: {count}")
    for x in range(int(count)):
        # print(f"x is {x}")
        jsonObj = json.loads(jsonData)  # Turns file json into object
        # By default, these requests will use random timestamps over the past 24 hours
        jsonObj["reqTimeSec"] = int(time.time()-random.randrange(1, 60))

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

    # Open for bulk request
    f = open("bulkFile.txt", "r")
    # Send the data to TrafficPeak and get response:
    sendBody = f.read(-1)
    r = requests.post(trafficPeak["ingestURL"],
                      data=sendBody, headers=headers, auth=auth)
    f.close
    print(f"File: {templateFileName} sent.\tCount: {count}\t\tResponse:{r.text}")
    return r.text


# Send general data. Several file types, mostly 200 responses
# myResponse = sendDataToTrafficPeak("ds2TemplateGeneralDataCached.json", 40000)

myResponse = sendDataToTrafficPeak("singleRequest.json", 100)
