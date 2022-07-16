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
from sprint4.sprint4_stack import TabraizSprint4Stack



class TabraizStage2(Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.stage = TabraizSprint4Stack(self,"TABAPPStack2")
