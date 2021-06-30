from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash

from crud import create_user, get_user_by_username
from database import get_db
from models import UserModel


class Register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="Username is required."
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Password is required."
    )

    def post(self):
        db = next(get_db())
        data = Register.parser.parse_args()

        if get_user_by_username(db, data['username']):
            return {"message": "The username is already taken."}, 400

        hashed_pwd = generate_password_hash(data['password'])
        new_user = UserModel(
            username=data['username'],
            hashed_password=hashed_pwd
        )
        try:
            create_user(db, new_user)
            return {"message": "The user was successfully created."}, 201
        except Exception:
            return {"message": "An error has occurred creating a user."}, 500
