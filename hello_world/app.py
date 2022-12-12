import json

from data.db import Database
from models.models import Base
from models.models import User


def lambda_handler(event, context):
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
        }),
    }
