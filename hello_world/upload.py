import base64
import json
from os import environ


def handler(event, context):
    body = base64.b64decode(event["body"])
    json_body = json.loads(body)

    filename = json_body["filename"]

    url = 'https://{}/{}/{}/{}'.format(
        event['headers']['Host'], event['requestContext']['stage'],
        environ.get('BUCKET_NAME'), filename
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "url": url,
        }),
    }
