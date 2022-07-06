from doctest import master
from aws_cdk import (
    Duration,
    RemovalPolicy,
    SecretValue,
    Stack,
    pipelines as pipeline_,
    aws_codepipeline_actions as actions_


    
)
from constructs import Construct




class MyPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        source = pipeline_.CodePipelineSource.git_hub("TabraizHassan1/sprint2","master",
        authentication = SecretValue.secrets_manager('tokenNew2'), trigger = actions_.GitHubTrigger('POLL')
        )
        synth = pipeline_.ShellStep("CodeBuild",
        input= source,
        commands= ['cd Tabraiz/sprint3/', 'pip install -r requirements.txt','cdk synth'],
        primary_output_directory= "Tabraiz/sprint3/cdk.out")

        myPipeline = pipeline_.CodePipeline(self, "TABPipeline",
        synth= synth)

        beta = 

