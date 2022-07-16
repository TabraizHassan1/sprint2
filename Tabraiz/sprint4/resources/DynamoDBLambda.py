from email import message
#from msilib import Table
from urllib import response
import boto3
import json
import os

#https://hands-on.cloud/working-with-dynamodb-in-python-using-boto3/
#client = boto3.client('dynamodb')


#https://www.infoq.com/news/2016/11/was-lambda-env-variables/
#accessing lambda environment variable
db_table_name=os.environ["DBTable"]
#all alarm information is in the event
def lambda_handler(event, context):
    #region = os.environ['AWS_REGION']
    db_resource = boto3.resource('dynamodb', region_name= 'us-east-1')    
    
    table = db_resource.Table(db_table_name)
    #parse event parameter to obtain relevant alarm information that you want to place in your DB
    Message = event['Records'][0]['Sns']['Message']
    Alarm_Name = event['Records'][0]['Sns']['MessageId']
    Alarm_Time = event['Records'][0]['Sns']['Timestamp']
   # md = json.loads(event['Records'][0]['Sns']['Message'])
    #Message = event['Records'][0]['Sns']['Message']
   # md = json.loads(event['Records'][0]['Sns']['Message'])
    #Metric_name= 
    #URL = 
   # Reason = event['Records'][0]['Sns']['Message']['NewStateReason']
    #TimeStamp = event['Records'][0]['Sns']['Timestamp']
    
    #insert the parsed information into the table
    response= table.put_item( #TableName = db_table_name,
    Item=
            {
             'Alarm_Name':  Alarm_Name,
              'Alarm_Time': Alarm_Time,
              'Message': Message,
               # 'Reason': {'S': Message ['NewStateReason']}
            #  'Metric_name': event['Records'][0]['Sns']['Message']["Trigger"]["MetricName"],
             # 'URL': event['Records'][0]['Sns']['Message']["Trigger"]["Dimensions"][0]["value"],
            
             #   'Reason': md ['NewStateReason']
                


    }

            )
    print("checking!!!!!")
    print("!!!!!!!!!!!!")
    print(event)
    return response





    
    

   


    
    




