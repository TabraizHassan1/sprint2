#!/usr/bin/env python3

import aws_cdk as cdk

from sprint4.pipeline_stack import TabraizPipelineStack
#from sprint4.sprint4_stack import TabraizSprint4Stack

app = cdk.App()
TabraizPipelineStack(app, "tabraizPipelineStackSprint4",)
#TabraizSprint4Stack(app, "tabraizPipelineStackSprint4",)

app.synth()
