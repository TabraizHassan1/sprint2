from cgitb import handler
from multiprocessing import reduction
from aws_cdk import (
    # Duration,
    RemovalPolicy,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as target_
    
)
from constructs import Construct



class Sprint1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create my lambda function for deploying hw_lamda.py
      
        hw_lambda = self.create_lambda("MyFirstLambda", "hw_lambda.lambda_handler","./resources")
        hw_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        # The code that defines your stack goes here

        #defining an event
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_events/README.html
        schedule = events_.Schedule.cron(minute="0/1")
        target = target_.LambdaFunction(handler= hw_lambda)
        rule = events_.Rule(self, "LambdaRuleEvent",
            description = 'this my rule to generate auto events for my hw_lamda', 
            schedule= schedule,           
            targets=[target]
           )
        # example resource
        # queue = sqs.Queue(
        #     self, "Sprint1Queue",
        #     visibility_timeout=Duration.seconds(300),
        # )


    #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html    
    def create_lambda(self,id_,handler, path):
                return lambda_.Function(self, id_,
                                runtime=lambda_.Runtime.PYTHON_3_7,
                                handler=handler,
                                code=lambda_.Code.from_asset(path)
)
