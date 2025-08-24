import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps({
            'level': 6,
            'type': 'Cloud Simulation',
            'service': 'AWS Lambda (LocalStack)',
            'timestamp': datetime.now().isoformat(),
            'message': 'Serverless computing simulation',
            'event': event
        })
    }
