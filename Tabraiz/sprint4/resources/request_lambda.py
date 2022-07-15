from asyncio.log import logger
from email import message
#from msilib import Table
from urllib import response
import boto3
import json
import os
import logging


#https://hands-on.cloud/working-with-dynamodb-in-python-using-boto3/
client = boto3.client('dynamodb')

db_resource = boto3.resource('dynamodb', region_name= 'us-east-1')    
table = db_resource.Table(db_table_name)




getMethod = 'GET'
postMethod = 'POST'
deleteMethod = 'DELETE'
patchMethod = 'PATCH'
urlpath = '/item' 
itemspath = '/items'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#https://www.infoq.com/news/2016/11/was-lambda-env-variables/
#accessing lambda environment variable
db_table_name=os.environ["RqTable"]
#all alarm information is in the event
def lambda_handler(event, context):
    #region = os.environ['AWS_REGION']
    


    logger.info(event)

    httpMethod = event['httpMethod']
    path = event['path']

    
    if(httpMethod== getMethod and path== urlpath):
        response = getItem(event['queryStringParameters']['URL_id'])
    elif(httpMethod== getMethod and path== itemspath):
        response = getItems()
    elif(httpMethod== postMethod and path== urlpath):
        response = saveItem(json.loads(event['body']))
    elif(httpMethod== patchMethod and path== urlpath):
        reqstBody = json.loads(event['body'])
        response = modifyItem(reqstBody['URL_id'], reqstBody['updateKey'], reqstBody['updateValue'])
    elif(httpMethod== deleteMethod and path== urlpath):
        reqstBody = json.loads(event['body'])
        response = deleteItem(reqstBody['URL_id'])
    else:
        repsonse = buildResponse(404, 'Not Found')

    return response



def getItem(urlid):
    try:
        response = table.get_item(

            Key = {
                'URL_id': urlid
            }
        )
        if 'item' in response:
            return buildResponse(200, response['item'])
        else:
            return buildResponse(404, {'Message': 'URL_id : %s not found' % urlid})
    except:
        logger.exception("Error!")




def getItems():
    try:
        response = table.scan()
        result = response ['item']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStarterKey = response['LastEvaluatedKey'])
            result.extend(response ['item'])
        body = {
            'url': response
        }
        return buildResponse(200,body)
    except:
        logger.exception("Error!")



def saveItem(rqstbody):
    try:
        table.put_item(item = rqstbody)
        
        

    






def buildResponse(statusCode, body= None):
    response={
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'

        }

    }
    if body is not None:
        response['body'] = json.dumps(body)
    return response



