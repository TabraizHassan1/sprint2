from multiprocessing import reduction
from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_
)
from constructs import Construct



class Sprint1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        hw_lambda = self.create_lambda("MyFirstLambda", "hw_lambda.lambda_handler","./resources")
        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "Sprint1Queue",
        #     visibility_timeout=Duration.seconds(300),
        # )
    def create_lambda(self,id_,handler, path ):
        return lambda_.Function(self, id_,
    runtime=lambda_.Runtime.PYTHON_3_7,
    handler=handler,
    code=lambda_.Code.from_asset(path)
)
