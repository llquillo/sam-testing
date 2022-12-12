import json
from data.db import Database
# import requests
from sqlalchemy import MetaData
from models.models import Base
from models.models import User

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    db = Database()

    if db._engine:
        Base.metadata.create_all(bind=db._engine)
        url_params = event["queryStringParameters"]
        user_id = int(url_params["user_id"])
        db.create_session()

        if db._session:
            user = db._session.query(User).get(user_id)

            json_body = {
                'id': user.id, 'email': user.email,
                'cognito_username': user.cognito_username
            }
            return {
                "statusCode": 200,
                "body": json.dumps(json_body)
            }
    return {
        "statusCode": 500,
        "body": json.dumps({
            "message": "Database not connected",
            # "location": ip.text.replace("\n", "")
        }),
    }
