import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest


from sprint4.sprint4_stack import TabraizSprint4Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint3/sprint3_stack.py
#def test_sqs_queue_created():
#    app = core.App()
#    stack = Sprint3Stack(app, "sprint3")
#    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

#https://towardsdatascience.com/make-your-python-tests-efficient-with-pytest-fixtures-3d7a1892265f
#Defining a pytest fixture for code optimization
@pytest.fixture
def template():
    app = core.App()
    stack = TabraizSprint4Stack(app, "sprint4")
    template = assertions.Template.from_stack(stack)
    return template



#Test for checking the lambda functions count 
def test_lambda_created(template):
    template.resource_count_is("AWS::Lambda::Function",3)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

def test_role_created(template):
    #check if roles are created or not
    #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    template.has_resource_properties(
        "AWS::IAM::Role",
            {
                "ManagedPolicyArns": [
                    {
                        "Fn::Join": [
                            "",
                            [
                                "arn:",
                                {
                                "Ref": "AWS::Partition"
                                },
                                ":iam::aws:policy/CloudWatchFullAccess"
                                ]
                            ]
                        },
                {
                    "Fn::Join": [
                    "",
                    [
                        "arn:",
                        {
                        "Ref": "AWS::Partition"
                        },
                        ":iam::aws:policy/AmazonDynamoDBFullAccess"
                        ]
                    ]
                }
            ]
        }
    )

def test_table_created(template):
    #check if table is created 
    #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    template.resource_count_is("AWS::DynamoDB::Table", 2)

def test_lambda_sub(template):
    #check if sns lambda subscription is created or not
    #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    template.has_resource_properties("AWS::SNS::Subscription", {"Protocol": "lambda"})


def test_email_sub(template):
    #check if email subscription has been created by user 
    #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    template.has_resource_properties("AWS::SNS::Subscription", {"Protocol": "email"})



#def test_to_json(test_app):
    #Test that the CloudFormation template deserialized into an object.
    #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.assertions/Template.html#aws_cdk.assertions.Template.to_json
#    test_app.to_json()


#Test for checking the api gateway count 
def test_countRestAPI(template):
      template.resource_count_is("AWS::ApiGateway::RestApi",1)

#Test for checking the api gateway resource property
#https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.assertions/Template.html#aws_cdk.assertions.Template.has_resource_properties
def test_resourceAPI(template):
     template.has_resource_properties("AWS::ApiGateway::Resource", {"PathPart": "item"})

#test for checking delete api method
#def test_DeleteAPImethod(template):
#     template.has_resource_properties("AWS::ApiGateway::Method", { "HttpMethod": "DELETE"})

#test for checking update api method
def test_UpdateAPImethod(template):
    template.has_resource_properties("AWS::ApiGateway::Method", { "HttpMethod": "POST"})

#test for checking put api method
#def test_PUTAPImethod(template):
#    template.has_resource_properties("AWS::ApiGateway::Method", { "HttpMethod": "PUT"})

#test for checking get api method
def test_UpdateAPImethod(template):
    template.has_resource_properties("AWS::ApiGateway::Method", { "HttpMethod": "GET"})
