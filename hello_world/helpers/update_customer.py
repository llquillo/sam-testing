import json

from data.db import Database
from models.models import Base
from models.models import User


def update_customer(user_id, updated_email):
    db = Database()

    if db._engine:
        Base.metadata.create_all(bind=db._engine)

        db.create_session()

        if db._session:
            user = db._session.query(User).get(user_id)

            if user:
                user.email = updated_email
                db._session.commit()

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
            "message": "User not found",
        }),
    }
