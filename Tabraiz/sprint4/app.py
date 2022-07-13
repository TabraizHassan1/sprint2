#!/usr/bin/env python3

import aws_cdk as cdk

from sprint4.pipeline_stack import MyPipelineStack


app = cdk.App()
MyPipelineStack(app, "tabraizPipelineStackSprint4")

app.synth()
