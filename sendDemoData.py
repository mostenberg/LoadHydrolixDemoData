
import requests
import json
import time
import random
import os
import gzip
import urllib
import logging
from urllib.parse import urlparse
import time

# Trying for bulk request


def compress_file(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        with gzip.open(output_file, 'wb') as f_out:
            f_out.writelines(f_in)


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
    file_size = os.stat("bulkFile.txt")

    # Now zip the file bulkfile.txt
    file_name = 'bulkFile.gz'

    # Create a gzip compressed file
    start_compress = time.time()
    with open('bulkFile.txt', 'rb') as f_in:
        with gzip.open(file_name, 'wb') as f_out:
            f_out.writelines(f_in)
    end_compress = time.time()
    compress_time = end_compress - start_compress

    # Specify the file name
    file_size_gz = os.stat(file_name)

    # Read the content of the gzipped file into a variable
    with open(file_name, 'rb') as file_content:
        content = file_content.read()

    # Additional headers for the request
    headers = {
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Content-Encoding': 'gzip',
        'User-Agent': 'YourApp/1.0',  # Replace with your application's user agent
    }

    response = requests.post(
        trafficPeak['ingestURL'], data=content, headers=headers, auth=auth)

    # Print the response
    print(response.text)
    # Send the data to TrafficPeak and get response:
    # sendBody = f.read(-1)
    # r = requests.post(trafficPeak["ingestURL"],
    #                  data=sendBody, headers=headers, auth=auth)
    # f.close

    # Report results
    print(
        f"File: {templateFileName} sent.\tCount: {count}\t\tResponse:{response.text}")
    print(
        f"\t\tUncompressed is: {file_size.st_size:,} , Compressed: {file_size_gz.st_size:,}, Ratio:{file_size.st_size/file_size_gz.st_size:,.1f}, CompressTime: {compress_time:,.2f} ")

    return response.text


start_time = time.time()

# Send general data. Several file types, mostly 200 responses
myResponse = sendDataToTrafficPeak("ds2TemplateGeneralDataCached.json", 40000)

# Send general uncached data. Several file types, mostly 200 responses
myResponse = sendDataToTrafficPeak("ds2TemplateGeneralDataUncached.json", 5000)

# Send data for some large files cached
myResponse = sendDataToTrafficPeak("ds2TemplateLargeFilesCached.json", 40000)

# Send data for some large files uncached
myResponse = sendDataToTrafficPeak("ds2TemplateLargeFilesUncached.json", 2000)

# Next, send some sample requests with errors 401,403,302 etc
myResponse = sendDataToTrafficPeak("ds2TemplateErrorRequests.json", 2000)

# Next, send some sample requests with errors 401,403,302 etc
myResponse = sendDataToTrafficPeak("ds2CMCDGood.json", 10000)


end_time = time.time()
# Calculate the overall execution time
execution_time = end_time - start_time

# Print the execution time
print(f"Overall execution time: {execution_time:.2f} seconds")
