import boto3
import json

from os import environ

def handler(event, context):

    sqs = boto3.client('sqs')
    print(event)