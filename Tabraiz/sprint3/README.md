
# Create, synthesize and deploy pipeline to automate Website Monitoring project - sprint 3 by tabraiz hassan!

[![Generic badge](https://img.shields.io/badge/OS-Mac%20OS-yellow)](#)   [![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)   [![Lambda](https://img.shields.io/badge/AWS-lambda-brightgreen)](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda.html)  [![Cloudwatch](https://img.shields.io/badge/AWS-cloudwatch-yellowgreen)](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch.html)  [![Sns](https://img.shields.io/badge/AWS-sns-orange)](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns.html) [![Dynamo](https://img.shields.io/badge/AWS-DynamoDB-blue)](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Table.html)   [![Virtual](https://img.shields.io/badge/-virtual%20env-green)](#)  [![made-for-VSCode](https://img.shields.io/badge/Made%20for-VSCode-1f425f.svg)](https://code.visualstudio.com/) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](#)      [![GitHub release](https://img.shields.io/github/release/Naereen/StrapDown.js.svg)](https://github.com/TabraizHassan1/sprint2/releases) [![Github all releases](https://img.shields.io/github/downloads/Naereen/StrapDown.js/total.svg)](https://github.com/TabraizHassan1/sprint2/releases)  [![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://GitHub.com/TabraizHassan1) [![Demo](https://img.shields.io/badge/-demo-red)](https://www.loom.com/share/833b3afe13124d3bb16993fece5fa1e1) [![Bash Shell](https://badges.frapsoft.com/bash/v1/bash.png?v=103)](https://github.com/ellerbrock/open-source-badges/)  [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

In sprint 2, we monitored the latency and availability of websites using serverless compute service (Lambda) and published the data in the metrices of Cloudwatch. The alarms were also deployed to help notify the user (using Sns service) via email in case the latency or availability value of the URL was below the threshold value. In addition to alarm notification to the user, the notification data was also stored in NoSQL database i.e. DynamoDB.

The objective of this sprint is to automate the process of Continuous Integration (CI) and Continuous Deployment (CD) by creating a pipeline. The pipeline consists of many stages having manual approval in the final production stage (in which the new version of application is deployed). Unit tests for the web crawler are also done in the pipeline stage to check for errors.

## Technologies

- Virtual environment: A python virtual environment is created and activated.
- AWS Lambda: A serverless compute service that runs when an event is invoked. We use lambda functions in our project
- AWS Cloudwatch: The latency and availability values are published using Cloudwatch services and can be seen in cloudwatch metrices. Cloudwatch is also used to monitor metrices for lambda resources.
- AWS Sns: AWS Sns(Simple notification service) is used to notify Cloud users, in case the alarms are generated.
- AWS DynamoDB: For future use, the notification data generated due to the alarms that are generated in case latency and availability values cross the threshold, is stored in a database.
- AWS Cdk Pipeline: The pipeline is used to automate the task of Continuous Integration (CI) and Continuous Deployment (CD)
- AWS Stage: Stages are used to perform test on application. In this sprint, beta and prod stages are created to check errors.
- AWS Code Deploy (Lambda Deployment Groups): In an AWS Lambda deployment, a deployment group defines a set of CodeDeploy configurations for future deployments of an AWS Lambda function. For example, the deployment group specifies how to route traffic to a new version of a Lambda function. It also might specify alarms and rollbacks.
- AWS cdk Assertions: Assertions are used in this sprint to perform unit tests on AWS resources.


## Setup

Download and install Visual Studio Code

Download and install python

Download, install and configure AWS CLI V2

Git clone from the shared link

### Create project directory

Create empty directories in your system:

```
$ mkdir Tabraiz && cd Tabraiz
$ mkdir sprint3 && cd sprint3
```

### cdk init

We will use cdk init to create a new Python CDK project:

```
$ cdk init sample-app --language python
```

### Activating the Virtualenv

To activate our virtualenv:

```
$ source .venv/bin/activate
```

Now that the virtual environment is activated, we install the required python modules:

```
$ python -m pip install -r requirements.txt
```

### NVM and NPM installation

We will install nvm and nmp:

```
$ nvm install v16.3.0 && nvm use v16.3.0 && nvm alias default v16.3.0
```

Then for npm cdk:

```
$ npm install -g aws-cdk
```

The `.venv` contains python virtual envirnment information. The `app.py` in the project folder is the 'main' for the sample application. It is the entry point for the app. The code in this file loads and instantiates an instance of class "tabraizPipelineStack" located in the folder sprint3/pipeline_stack.py. The `pipeline_stack` then connects, `pipeline_stage.py` with `sprint3_stack.py`


### Pytest

To add additional dependencies like pytest, we use:

```
$ python -m pip install -r requirements-dev.txt
```
To use pytest or to manually check the unit test results, we use:

```
$ pytest
```


## Working overview

### Latency,Availability and Cloudwatch

Firstly, latency(the amount of delay on a network) and availibilty(whether the webpage is up or down) values for each of the four URLs defined in our `constants.py` are generated using GET response and published on cloudwatch in cloudwatch metrices. For availability value,the GET response value is '200' when the website is available and the output '1.0' is stored in availbility metric; '0' is stored in case the GET response does not return '200'. Similarly, the GET response is also used to calculate latency value. All of the availbility and latency values are put in metrices and published to cloudwatch in the file `cloudWatch_putMetric.py`


### Alarm, Sns and DynamoDB

Alarms and Sns notification service is defined in our `sprint3_stack.py` file, as they are part of our infrastructure. Alarms are generated in case, the cloudwatch metrice value of availibility is less than 1 or the latency value is greater than 0.2. As soon as alarms are generated, they are notified to the user using Sns service to its subscribers via email. The alarm data (i.e. alarm name, alarm time and the complete message) is stored to cloud DynamoDB database defined in the `DynamoDBLambda.py`.

The alarms are also generted and notified to the user in case, the threshold values of lambda duration metric and lambda invocation metrics cross the threshold.


### Pipeline

To automate our build through various stages like build, test and deploy, etc. we performed the following steps:
* Created a pipeline
* Create and add beta stage to pipeline with a pre testing step
* Create and add prod stage to pipeline with a pre testing step and manual approval step for deployment
* Create unit tests
* Create metrices for lambda duration and invocations to be published on cloudwatch and generate alarm notifications
* Lambda Deployment Configurations and Roll Back
* Synthesize and then deploy to AWS account


## Demo

To watch demo: [![Demo](https://img.shields.io/badge/-demo-red)](https://www.loom.com/share/833b3afe13124d3bb16993fece5fa1e1)

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk destroy`     destroys the stack
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

## API Reference

A list of all the references to the resources used to build this project:

* [AWS CDK CloudWatch](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch.html)
* [AWS CDK CloudWatch Actions](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch_actions.html)
* [AWS CDK Events](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_events.html)
* [AWS CDK Events Targets](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_events_targets.html)
* [AWS CDK IAM](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam.html)
* [AWS CDK Lambda](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda.html)
* [AWS CDK SNS](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns.html)
* [AWS CDK SNS Subscriptions](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns_subscriptions.html)
* [DynamoDB table](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Table.html)
* [AWS CDK ShellStep](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/ShellStep.html#aws_cdk.pipelines.ShellStep)
* [AWS CDK CodePipeline](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipeline.html)
* [AWS CDK AddStageOpts](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/AddStageOpts.html#addstageopts)
* [AWS CDK CodePipelineSource](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipelineSource.html)
* [AWS CDK LambdaDeploymentGroup](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codedeploy/LambdaDeploymentGroup.html#aws_cdk.aws_codedeploy.LambdaDeploymentGroup)
