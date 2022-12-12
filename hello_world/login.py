import boto3
import json
from os import environ


def handler(event, context):
    """ Retrieves access token for a Cognito user """
    print(event)
    status_code = 400
    response_data = None
    request_body = json.loads(event["body"])
    print(request_body)
    if request_body:
        print("Inside if!!")
        username = request_body['username']
        password = request_body['password']
        auth_data = {'USERNAME': username, 'PASSWORD': password}
        try:
            print("logging in...")
            provider_client = boto3.client('cognito-idp', region_name=environ.get('AWS_REGION'))
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
