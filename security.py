from werkzeug.security import check_password_hash

from crud import get_user_by_username, get_user_by_id
from database import get_db


def authenticate(username, password):
    user = get_user_by_username(next(get_db()), username)
    if user and check_password_hash(user.hashed_password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return get_user_by_id(next(get_db()), user_id)
