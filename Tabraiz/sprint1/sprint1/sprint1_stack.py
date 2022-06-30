from cgitb import handler
from multiprocessing import reduction
from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_events as events_,
    aws_iam as aws_iam,
    aws_events_targets as target_,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns_,
    aws_cloudwatch_actions as cw_actions,
    aws_sns_subscriptions as subscriptions_,
    aws_dynamodb as db_

    
)
from constructs import Construct
from resources import constants as constants



class Sprint1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create my lambda function for deploying hw_lamda.py

        lambda_role = self.create_lambda_role()
      
        hw_lambda = self.create_lambda("MyFirstLambda", "hw_lambda.lambda_handler","./resources", lambda_role)
        db_lambda = self.create_lambda("TabDynamoDBLambdaFunction", "DynamoDBLambda.lambda_handler","./resources", lambda_role)
        hw_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        db_lambda.apply_removal_policy(RemovalPolicy.DESTROY)



        #create a dynamo DB table
        DBTable = self.create_table()

        #get table name
        dbName = DBTable.table_name

        #creating a db lambda environment variable
        #https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-samples
        db_lambda.add_environment("DBTable", dbName)




        # The code that defines your stack goes here

        #defining an event
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_events/README.html
        schedule = events_.Schedule.cron() #every minute
        target = target_.LambdaFunction(handler= hw_lambda)
        rule = events_.Rule(self, "LambdaRuleEvent",
            description = 'this my rule to generate auto events for my hw_lamda', 
            schedule= schedule,           
            targets=[target]
           )

        rule.apply_removal_policy(RemovalPolicy.DESTROY)


        #Creating my sns topic(i.e. message server)
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns/Topic.html
        topic = sns_.Topic(self, "AlarmNotification")
        topic.apply_removal_policy(RemovalPolicy.DESTROY)

        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns_subscriptions/EmailSubscription.html
        topic.add_subscription(subscriptions_.EmailSubscription('tabraiz.hassan.skipq@gmail.com'))
        topic.add_subscription(subscriptions_.LambdaSubscription(db_lambda))
        





        # example resource
        # queue = sqs.Queue(
        #     self, "Sprint1Queue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        for i in constants.URL_TO_MONITOR:
            dimensions = {"URL": i}
            #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
            #define threshold and create alarms
            availMetric = cloudwatch_.Metric(metric_name= constants.URL_MONITOR_METRIC_NAME_AVAILABILITY,
            namespace= constants.URL_MONITOR_NAMESPACE,
            dimensions_map=dimensions,
            period=Duration.minutes(1))


            #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
            availAlarm = cloudwatch_.Alarm(self, "Availability Alarm For "+ i,
            comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
            threshold=0,
            evaluation_periods=1,
            metric=availMetric,
            
                )

            
            


        

            #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
            #define threshold and create alarms
            latenMetric = cloudwatch_.Metric(metric_name= constants.URL_MONITOR_METRIC_NAME_LATENCY,
            namespace= constants.URL_MONITOR_NAMESPACE,
            dimensions_map=dimensions,
            period=Duration.minutes(1))


            #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
            latenAlarm = cloudwatch_.Alarm(self, "Latency Alarm For "+ i,
            threshold=0.2,
            evaluation_periods=1,
            metric=latenMetric,
        

            )

            #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
            availAlarm.add_alarm_action(cw_actions.SnsAction(topic))
            latenAlarm.add_alarm_action(cw_actions.SnsAction(topic))


            availAlarm.apply_removal_policy(RemovalPolicy.DESTROY)
            latenAlarm.apply_removal_policy(RemovalPolicy.DESTROY)
            



    #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html    
    def create_lambda(self,id_,handler, path, role):
                return lambda_.Function(self, id_,
                                runtime=lambda_.Runtime.PYTHON_3_7,
                                handler=handler,
                                code=lambda_.Code.from_asset(path),
                                role= role,
                                timeout= Duration.seconds(120)
                                        )

    def create_lambda_role(self):
        #Create a role
        lambdaRole = aws_iam.Role(self, "lambda-role", 
                    assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                    managed_policies = [
                       # aws_iam.iam.ManagedPolicy.from_managed_policy_name( 'service-role/AWSLambdaBasicExecutionRole')    ---This is default given
                        aws_iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                        aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
                    ])
        return lambdaRole
    
    #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Table.html
    #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Attribute.html#aws_cdk.aws_dynamodb.Attribute
    def create_table(self):
        return db_.Table(
            self, id = "AlarmInfoTable",
            partition_key = db_.Attribute(name="Alarm_Name", type=db_.AttributeType.STRING),
            sort_key = db_.Attribute(name= "Alarm_Time", type=db_.AttributeType.STRING),
            removal_policy= RemovalPolicy.DESTROY,
        )