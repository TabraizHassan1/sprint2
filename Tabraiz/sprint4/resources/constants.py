#import boto3
#import json

#namespace for metrices
URL_MONITOR_NAMESPACE = "TABWebHealthNS"
#get data on availability and latency of the urls
URL_MONITOR_METRIC_NAME_AVAILABILITY = "url_availability"
URL_MONITOR_METRIC_NAME_LATENCY = "url_latency"
URL_TO_MONITOR = []
""""
def get_url_list(db_table_name):
    #table_name= "RqTable"
    db_resource = boto3.resource('dynamodb', region_name= 'us-east-1')  
    
    table = db_resource.Table(db_table_name)
    result = table.scan()
    response = result['items']
    #url names to monitor

   
    for i in range(len(response)):
        URL_TO_MONITOR.append(response[i]["URL"])
    
    return URL_TO_MONITOR

"""
