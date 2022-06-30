
# Website Monitoring project - sprint 2 by tabraiz hassan!

[![Generic badge](https://img.shields.io/badge/OS-Mac%20OS-yellow)](#)   [![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)   [![Lambda](https://img.shields.io/badge/AWS-lambda-brightgreen)](#)  [![Cloudwatch](https://img.shields.io/badge/AWS-cloudwatch-yellowgreen)](#)  [![Sns](https://img.shields.io/badge/AWS-sns-orange)](#) [![Dynamo](https://img.shields.io/badge/AWS-DynamoDB-blue)](#)   [![Virtual](https://img.shields.io/badge/-virtual%20env-green)](#)  [![made-for-VSCode](https://img.shields.io/badge/Made%20for-VSCode-1f425f.svg)](https://code.visualstudio.com/) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](#)      [![GitHub release](https://img.shields.io/github/release/Naereen/StrapDown.js.svg)](https://GitHub.com/Naereen/StrapDown.js/releases/) [![Github all releases](https://img.shields.io/github/downloads/Naereen/StrapDown.js/total.svg)](https://GitHub.com/Naereen/StrapDown.js/releases/)  [![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://GitHub.com/TabraizHassan1) [![Demo](https://img.shields.io/badge/-demo-red)](#) [![Bash Shell](https://badges.frapsoft.com/bash/v1/bash.png?v=103)](https://github.com/ellerbrock/open-source-badges/)  [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

The objective of this sprint is to monitor latency and availability of website using serverless compute service (Lambda) and publish the data in the metrices of Cloudwatch. The alarms are also deployed to help notify the user (using Sns service) via email in case the latency or availability value of the URL is below the threshold value. In addition to alarm notification to the user, the notification data is also stored in NoSQL database i.e. DynamoDB

## Technologies

- Virtual environment: A python virtual environment is created and activated.
- AWS Lambda: A serverless compute service that runs when an event is invoked. We use lambda functions in our project
- AWS Cloudwatch: The latency and availability values are published using Cloudwatch services and can be seen in cloudwatch metrices.
- AWS Sns: AWS Sns(Simple notification service) is used to notify Cloud users, in case the alarms are generated.
- AWS DynamoDB: For future use, the notification data generated due to alarms is stored in a database.




## Setup

Download and install Visual Studio Code

Download and install python

Download, install and configure AWS CLI V2

Git clone from the shared link

### Create project directory

Create empty directories in your system:

```
$ mkdir Tabraiz && cd Tabraiz
$ mkdir sprint1 && cd sprint1
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

The `.venv` contains python virtual envirnment information. The `app.py` in the project folder is the 'main' for the sample application. It is the entry point for the app. The code in this file loads and instantiates an instance of class "tabraizSprint1Stack" located in the folder sprint1/sprint1_stack.py. The `sprint1_stack.py` is a custom CDK stack construct that is to be used in our CDK application. It is the main stack.


## Working overview

### Latency,Availability and Cloudwatch

Firstly, latency(the amount of delay on a network) and availibilty(whether the webpage is up or down) values for each of the four URLs defined in our `constants.py` are generated using GET response and published on cloudwatch in cloudwatch metrices. For availability value,the GET response value is '200' when the website is available and the output '1.0' is stored in availbility metric; '0' is stored in case the GET response does not return '200'. Similarly, the GET response is also used to calculate latency value. All of the availbility and latency values are put in metrices and published to cloudwatch in the file `cloudWatch_putMetric.py`


### Alarm, Sns and DynamoDB

Alarms and Sns notification service is defined in our `sprint1_stack.py` file, as they are part of our infrastructure. Alarms are generated in case, the cloudwatch metrice value of availibility is less than 1 or the latency value is greater than 0.2. As soon as alarms are generated, they are notified to the user using Sns service to its subscribers via email. The alarm data (i.e. alarm name, alarm time and the complete message) is stored to cloud DynamoDB database defined in the `DynamoDBLambda.py`



## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk destroy`     destroys the stack
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

API Reference

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
