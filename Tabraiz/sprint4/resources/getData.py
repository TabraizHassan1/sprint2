import boto3
import json
import os

#https://hands-on.cloud/working-with-dynamodb-in-python-using-boto3/
#client = boto3.client('dynamodb')

db_resource = boto3.resource('dynamodb', region_name= 'us-east-1')  
#https://www.infoq.com/news/2016/11/was-lambda-env-variables/
#accessing lambda environment variable



#function to get url list from database and return the url names in a list
def get_url_list(table_name):
    #table_name= "RqTable"
    table = db_resource.Table(table_name)
    result = table.scan()
    response = result['items']
    #url names to monitor
    URL_TO_MONITOR = []
   
    for i in range(len(response)):
        URL_TO_MONITOR.append(response[i]["URL"])
    
    return URL_TO_MONITOR

