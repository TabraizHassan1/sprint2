 
from datetime import datetime
import http
import urllib3
from urllib import response



URL_TO_MONITOR = 'skipq.org'


def lambda_handler(event, context):
    print("hello world")
    # i want to contain my latency and availablity metrics for my webresource
    values= dict()
    availability = getAvailability()
    latency= getLatency()
    values.update({"availability": availability, "Latency": latency})

    print(values)




#describe the parameters that your function takes
#mention the return value
def getAvailability():
    http = urllib3.PoolManager()
    response = http.request("GET", URL_TO_MONITOR)
    if response.status == 200:
        return 1.0
    else:
        return 0.0





#describe the parameters that your function takes
#mention the return value
def getLatency():
     http = urllib3.PoolManager()
     start = datetime.now()
     response = http.request("GET", URL_TO_MONITOR)
     end = datetime.now()
     delta = end - start                        #take time difference
     latencySec = round(delta.microseconds * 0.000001,6)
     return latencySec

