import boto3
import json
from os import environ

import constants as const
from helpers.update_customer import update_customer


def handler(event, context):
    sqs = boto3.client('sqs')
    print(event)
    for record in event['Records']:
        receipt_handle = record.get('receiptHandle')
        message_payload = json.loads(record.get('body'))
        message_type = message_payload.get('type')
        handler_result = None

        if message_type == const.UPDATE_INFO:
            body = message_payload.get('body')
            handler_result = update_customer(body['id'], body['updated_email'])
        elif message_type == const.PROCESS_B:
            print("Process B")

    if handler_result:
        sqs.delete_message(
            QueueUrl=environ.get('SQS_QUEUE_URL'), ReceiptHandle=receipt_handle
        )

    return event
