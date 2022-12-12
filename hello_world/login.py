import base64
import boto3
import json
from os import environ


def handler(event, context):
    """ Retrieves access token for a Cognito user """
    status_code = 400
    response_data = None
    credentials = event["body"]
    decoded_creds = base64.b64decode(credentials)
    request_body = json.loads(decoded_creds)

    if request_body:

        username = request_body['username']
        password = request_body['password']
        auth_data = {'USERNAME': username, 'PASSWORD': password}
        try:
            provider_client = boto3.client(
                'cognito-idp', region_name=environ.get('AWS_REGION')
            )
            resp = provider_client.admin_initiate_auth(
                UserPoolId=environ.get('USERPOOL_ID'),
                AuthFlow='ADMIN_USER_PASSWORD_AUTH',
                AuthParameters=auth_data,
                ClientId=environ.get('TOKEN_CLIENT_ID'))
            token = resp['AuthenticationResult']['IdToken']
            response_data = {'access_token': token}
            status_code = 200
        except Exception as err:
            status_code = 403
            response_data = {'error': '{}'.format(str(err))}
    else:
        response_data = {'error': 'Missing request body'}
    return {
        "statusCode": status_code,
        "body": json.dumps(response_data)
    }
