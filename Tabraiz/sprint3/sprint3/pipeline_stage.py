import imp
from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_,
    Stage
 

    
)
from constructs import Construct
from sprint3.sprint3_stack import Sprint3Stack



class MyStage(Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.stage = Sprint3Stack(self,"TABAPPStack")
