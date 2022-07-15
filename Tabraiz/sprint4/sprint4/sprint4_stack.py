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
    aws_dynamodb as db_,
    aws_codedeploy as codedeploy_,
    aws_apigateway as apigateway_

    
)
from constructs import Construct
from resources import constants as constants



class Sprint4Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create my lambda function for deploying hw_lamda.py

        lambda_role = self.create_lambda_role()
      
        hw_lambda = self.create_lambda("MyFirstLambda", "hw_lambda.lambda_handler","./resources", lambda_role)
        db_lambda = self.create_lambda("TabDynamoDBLambdaFunction", "DynamoDBLambda.lambda_handler","./resources", lambda_role)
        hw_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        db_lambda.apply_removal_policy(RemovalPolicy.DESTROY)




        #lambda creation and destruction
        rq_lambda = self.create_lambda("TABRequestLambda", "request_lambda.lambda_handler","./resources", lambda_role)
        rq_lambda.apply_removal_policy(RemovalPolicy.DESTROY)


        #create gateway
        api_connect = self.create_api("request_lambda.lambda_handler")
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaRestApi.html
        item = api_connect.root.add_resource("item")
        item.add_method("GET") # GET /item
        item.add_method("POST") # POST /item
        item.add_method("PATCH") # PATCH /item
        item.add_method("DELETE") # DELETE /item

        items = api_connect.root.add_resource("items")
        items.add_method("GET") # GET /items






        api_connect.apply_removal_policy(RemovalPolicy.DESTROY)


        #Creating my sns topic(i.e. message server)
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns/Topic.html
        topic = sns_.Topic(self, "AlarmNotification")
        topic.apply_removal_policy(RemovalPolicy.DESTROY)

        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns_subscriptions/EmailSubscription.html
        topic.add_subscription(subscriptions_.EmailSubscription('tabraiz.hassan.skipq@gmail.com'))
        topic.add_subscription(subscriptions_.LambdaSubscription(db_lambda))



        #Step 1: Get my metric
        #(A):
     #   hw_lambdaMetric = hw_lambda.metric('Duration')

        #(B):
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        hw_lambdaDurMetric = hw_lambda.metric_duration()

        #(C):
        #dimensions = {"FunctionName": hw_lambda.function_name}
        #hw_lambdaMetric = cloudwatch_.Metric(metric_name= 'Duration',
        #    namespace= 'AWS/Lambda',
        #    dimensions_map=dimensions,
        #    period=Duration.minutes(1))

                

        #Step 2: Create Alarm for my Lambda duration Metric

        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
        durationAlarm = cloudwatch_.Alarm(self, "hw_lambda_DurationAlarm ",
        comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
        threshold=8000,
        evaluation_periods=1,
        metric=hw_lambdaDurMetric )

        #Removal policy for duration alarm
        durationAlarm.apply_removal_policy(RemovalPolicy.DESTROY)





        hw_lambdaInvocMetric = hw_lambda.metric_invocations()
        #Step 2: Create Alarm for my Lambda invocation Metric
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
        invocAlarm = cloudwatch_.Alarm(self, "hw_lambda_InvocationAlarm ",
        comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
        threshold=1,
        evaluation_periods=1,
        metric=hw_lambdaInvocMetric )

        #Removal policy for invocation alarm
        invocAlarm.apply_removal_policy(RemovalPolicy.DESTROY)

        #Conneting Duration and Invocation Alarms to the SNS Topic
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
        durationAlarm.add_alarm_action(cw_actions.SnsAction(topic))
        invocAlarm.add_alarm_action(cw_actions.SnsAction(topic))



        #Deployment Configuration for Lambda Deployment Group 
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/LambdaDeploymentConfig.html    
        version = hw_lambda.current_version
        alias = lambda_.Alias(self, "LambdaAlias",
        alias_name="Prod",
        version=version)     
        #Lambda deployment configurations and rollback
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/LambdaDeploymentGroup.html 
        #Lambda group specifies how to route traffic to a new  version of lambda, it might also specify how alarms will be geneerated and how to roll back
        deployment_group = codedeploy_.LambdaDeploymentGroup(self, "HwLambdaDeployment",
        alarms=[durationAlarm,invocAlarm],
        alias=alias,                  #default auto rollback
        deployment_config=codedeploy_.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE) #after every one minute on 10 percent instances, the new version is deployed


        






        #create a dynamo DB table
        DBTable = self.create_table()
        #2nd table
        DBTable2 = self.create_table2()

        #get table name
        dbName = DBTable.table_name
        #get 2nd table name
        dbName2 = DBTable2.table_name

        #creating a db lambda environment variable
        #https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-samples
        db_lambda.add_environment("DBTable", dbName)
        #2nd table environment variable
        rq_lambda.add_environment("RqTable",dbName2)



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
            threshold=1,
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

    #2nd table to store url data
    #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Table.html
    #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Attribute.html#aws_cdk.aws_dynamodb.Attribute
    def create_table2(self):
        return db_.Table(
            self, id = "URLInfoTable",
            partition_key = db_.Attribute(name="URL_id", type=db_.AttributeType.STRING),
            removal_policy= RemovalPolicy.DESTROY,
        )    
    
    def create_api(self, handler):
        return apigateway_.LambdaRestApi(self, "URLApi", handler= handler, proxy=False, )