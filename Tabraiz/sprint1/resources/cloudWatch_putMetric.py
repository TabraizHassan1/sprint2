import boto3


 #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html

 
class cloudWatch_putMetric:
    def __init__(self):
        self.client = boto3.client('cloudwatch')
        

    

    def put_data(self, nameSpace, metricNAme, dimension, value):
         response = self.client.put_metric_data(
         Namespace=nameSpace,
        MetricData=[
        {
            'MetricName': metricNAme,
            'Dimensions': dimension,
            'Value' :  value,

            
           }
    ])
    