 
from datetime import datetime

import http
import urllib3
from urllib import response

from cloudWatch_putMetric import cloudWatch_putMetric

import constants as constants




def lambda_handler(event, context):
    print("hello world")
    # i want to contain my latency and availablity metrics for my webresource
    values= dict()
    #i would like to publish my matrices to cloudwatch
    cw= cloudWatch_putMetric()
    
    for i in constants.URL_TO_MONITOR:
        availability = getAvailability(i)
        latency= getLatency(i)
        
        values.update({"availability": availability, "Latency": latency})
        print(values)


        dimension = [ { 'Name': 'URL', 'Value': i}]


        responseAvail = cw.put_data(constants.URL_MONITOR_NAMESPACE,
        constants.URL_MONITOR_METRIC_NAME_AVAILABILITY,
        dimension,
        availability
            )
        responseLat = cw.put_data(constants.URL_MONITOR_NAMESPACE,
        constants.URL_MONITOR_METRIC_NAME_LATENCY,
        dimension,
        latency
            )
  
    #create alarms and define threshold
   
#describe the parameters that your function takes
#mention the return value
#returns boolean value either 0 or 1
def getAvailability(url):
    http = urllib3.PoolManager()
    response = http.request("GET", url)
    if response.status == 200:
        return 1.0
    else:
        return 0.0





#describe the parameters that your function takes
#mention the return value
#returns the latency value of the url
def getLatency(url):
     http = urllib3.PoolManager()
     start = datetime.now()
     response = http.request("GET", url)
     end = datetime.now()
     delta = end - start                        #take time difference
     latencySec = round(delta.microseconds * 0.000001,6)
     return latencySec

