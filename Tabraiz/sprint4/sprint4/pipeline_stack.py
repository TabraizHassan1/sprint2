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
from sprint4.pipeline_stage import MyStage




class MyPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/README.html
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipelineSource.html
        #https://docs.aws.amazon.com/cli/latest/reference/secretsmanager/create-secret.html
        #Providing a GitHub Source as the codepipeline source (source stage)
        source = pipeline_.CodePipelineSource.git_hub("TabraizHassan1/sprint2","main",
        authentication = SecretValue.secrets_manager('tokenNew2'), trigger = actions_.GitHubTrigger('POLL')
        )


        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodeBuildStep.html
        #Code Build step (build stage)
        synth = pipeline_.ShellStep("CodeBuild",
        input= source,
        commands= ['cd Tabraiz/sprint4/', 'pip install -r requirements.txt','npm install -g aws-cdk','cdk synth'],
        primary_output_directory= "Tabraiz/sprint3/cdk.out")


        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipeline.html
        #Creating a code pipeline to deploy cdk apps
        myPipeline = pipeline_.CodePipeline(self, "TABPipeline",
        synth= synth)


       

        # Create and add beta stage to pipeline with a pre testing step (Pre-production beta Stage for validation)
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/AddStageOpts.html
        beta = MyStage(self, "TABBetaStage")
        myPipeline.add_stage(beta, pre=[pipeline_.ShellStep("UnitTest",
        commands= ['cd Tabraiz/sprint4/', 'pip install -r requirements.txt','pip install -r requirements-dev.txt','npm install -g aws-cdk','cdk synth', 'pytest'],
        primary_output_directory= "Tabraiz/sprint4/cdk.out")
                ])

        #Create  production stage
        prod = MyStage(self, "TABProdStage")
        #Add production stage to pipeline with a pre manual approval step
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/ManualApprovalStep.html
        myPipeline.add_stage(prod, pre=[pipeline_.ManualApprovalStep("PromoteToProduction")])


        #myPipeline.add_stage(prod)

