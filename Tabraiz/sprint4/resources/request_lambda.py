#from asyncio.log import logger
#from email import message
#import re
#from msilib import Table
#from urllib import response
import boto3
import json
import os
from boto3.dynamodb.conditions import Key
#import logging


#https://hands-on.cloud/working-with-dynamodb-in-python-using-boto3/
#client = boto3.client('dynamodb')


db_resource = boto3.resource('dynamodb', region_name= 'us-east-1')    
#https://www.infoq.com/news/2016/11/was-lambda-env-variables/
#accessing lambda environment variable
db_table_name=os.environ["RqTable"]
table = db_resource.Table(db_table_name)

#itemspath = '/items'
#logger = logging.getLogger()
#logger.setLevel(logging.INFO)


getMethod = 'GET'
postMethod = 'POST'
deleteMethod = 'DELETE'
putMethod = 'PUT'
urlpath = '/item' 
#all alarm information is in the event
def lambda_handler(event, context):
    #region = os.environ['AWS_REGION']
    #logger.info(event)
    httpMethod = event['httpMethod']
    #path = event['path']
    if(httpMethod== getMethod):
        response = getItem()
   # elif(httpMethod== getMethod and path== itemspath):
   #     response = getItems()
    elif(httpMethod== postMethod):
        response = saveItem(json.loads(event['body']))
        
    elif(httpMethod== putMethod):
        #reqstBody = json.loads(event['body'])
        #response = modifyItem(reqstBody['URL_id'],reqstBody['URL_name'])
        response = modifyItem(json.loads(event['body']))

    elif(httpMethod== deleteMethod):
        #reqstBody = json.loads(event['body'])
        #response = deleteItem(reqstBody['URL_id'])
        response = deleteItem(json.loads(event['body']))

    else:
        return{
        'statusCode': 404,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'},
        'body': json.dumps('Not found')
        }

    return response




#GET/Read url from database
def getItem():
    response = table.scan()['Items']
    if response:
        return buildResponse(response)
    else:
        return buildResponse({"Message":"No URL found!!!"})
 #  except:
  #      logger.exception("Error!")



#Save url in database
def saveItem(rqstbody):
    url_id= rqstbody['URL_id']
    url_name = rqstbody['url_name']
    key ={
        'URL_id' : str(url_id),
        'url_name': url_name


    }
    response=table.put_item(Item = key)
    if response:
        return buildResponse({"Message":"URL Added successfully!!!"})
    else:
        return buildResponse({"Message":"URL cannot be added error!!!"})
    


#update url by id 
def modifyItem(reqstBody):
    url_id= reqstBody['URL_id']
    url_name = reqstBody['url_name']
   # Key = {
   #     'URL_id' : str(url_id)
   # }
    response = table.update_item(
    Key = {
        'URL_id' : str(url_id)
    },
    UpdateExpression = 'SET #url_name = :url_name',
    ExpressionAttributeValues={':url_name': url_name },
    ExpressionAttributeNames = {"#url_name": "url_name"}

    )
    if response:
        return buildResponse({"Message":"URL Updated successfully!!!"})
    else:
        return buildResponse({"Message":"URL cannot be updated error!!!"})



#delete url by id
def deleteItem(reqstBody):
    url_id= reqstBody['URL_id']
    #Key = 
    response = table.delete_item( 
        Key = {
        'URL_id' : str(url_id)
        } )
    #Key )
    if response:
        return buildResponse({"Message":"URL Deleted successfully!!!"})
    else:
        return buildResponse({"Message":"URL cannot be deleted error!!!"})





#return response function
def buildResponse(response_data):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'

        },
        'body': json.dumps(response_data)

    }




















""""
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

"""





