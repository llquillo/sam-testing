import json

from data.db import Database
from models.models import User


def handler(event, context):
    """ Lambda handler entry point """

    db = Database()
    db.create_session()

    username = event["userName"]
    cognito_request = event["request"]
    user_attributes = cognito_request['userAttributes']

    user = User(
        email=user_attributes["email"], cognito_username=username,
    )
    if db._session:
        try:
            db._session.add(user)
            db._session.commit()
        finally:
            db._session.close()
