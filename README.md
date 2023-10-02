# Overview

This Python code allows you to send simulated DataStream 2 data to a Hydrolix ingest URL to provide sample data for demoing the TrafficPeak dashboards and data.

## Files

sendDemoData.py : Main file. Run this python file to send demo data for past 24 hours to your TrafficPeak ingest url
ds2TemplateErrorRequests.json : Has requests which are mostly returning error responses (403,5)
ds2TemplateGeneralData.json : Has general request paths (css,jpg,html etc), mostly 200 responses, typcial file sizes
ds2TemplateLargeFiles.json : Has very large files.

## Usage

Download the repository to your local directory.

Create a file named 'trafficPeakParams.json' in the main directory. This file should contain your trafficPeak ingest URL, username and password in the following format:

```{
  "ingestURL": "https://iad.trafficpeak.live/ingest/event?table=Akamai_Dashboard_Development.logs&token=fd1fc711542axxxxyyyyxxxxyyyyxxxxyyab823d274",
  "username": "<ingestUsernameHere>",
  "password": "<ingestpasswordHere>"
}
```

Then run the file sendDemoData.py . This file will load data into your ingest endpoint for the past 24 hours.
Currently it's set to load 21k requests, with a combination of general files, large files and error files.
Plan is to add special purpose datasets also to allow demoing how to 'find' issues (i.e. items with low cache rate, bots etc)

## Configuring

### Debugging
