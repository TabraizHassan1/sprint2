#!/usr/bin/env python3

import aws_cdk as cdk

from sprint4.pipeline_stack import TabraizPipelineStack


app = cdk.App()
TabraizPipelineStack(app, "tabraizPipelineStackSprint4",)

app.synth()
