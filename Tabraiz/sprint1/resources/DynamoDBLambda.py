from email import message
import boto3
import os

#https://hands-on.cloud/working-with-dynamodb-in-python-using-boto3/
db_client = boto3.resource('dynamodb')

#https://www.infoq.com/news/2016/11/was-lambda-env-variables/
#accessing lambda environment variable
db_table_name=os.environ["DBTable"]



#all alarm information is in the event
def lambda_handler(MyEvent, context):

    table = db_client.Table(db_table_name)

     
    #parse event parameter to obtain relevant alarm information that you want to place in your DB
    AlarmName = MyEvent["Records"][0]["Sns"]["MessageId"]
    Message = MyEvent["Records"][0]["Sns"]["Message"]
    TimeStamp = MyEvent["Records"][0]["Sns"]["Timestamp"]
    
    #insert the parsed information into the table
    table.put_item( TableName = db_table_name,
    Item=
            {
                "Alarm_name" :{"S": AlarmName},
                "Message" :{"S": Message},
                "Time_stamp" :{"S": TimeStamp}


    }

    )

    print("checking!!!!!")
    print("!!!!!!!!!!!!")
    print(MyEvent)
    return table





    
    

   


    
    




