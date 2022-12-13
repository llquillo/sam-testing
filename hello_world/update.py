import base64
import boto3
import json
import constants as const

from os import environ


def handler(event, context):
    body = base64.b64decode(event['body'])
    json_body = json.loads(body)
    url_params = event["queryStringParameters"]
    user_id = int(url_params["user_id"])

    customer_info = {
        'id': user_id,
        'updated_email': json_body['updated_email']
    }

    queue_message = {
        'type': const.UPDATE_INFO,
        'body': customer_info
    }

    sqs = boto3.client('sqs')
    sqs.send_message(
        QueueUrl=environ.get('SQS_QUEUE_URL'),
        MessageBody=str(
            json.dumps(queue_message)
        ),
        MessageGroupId=const.UPDATE_INFO
    )

    return {
        "statusCode": 204,
        "body": None
    }
