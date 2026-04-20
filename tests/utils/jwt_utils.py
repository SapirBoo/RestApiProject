import jwt
import os
from datetime import datetime, timedelta

SECRET_KEY = os.environ.get("SECRET_KEY", "test-secret")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")

def create_token(user_id: int, expires_delta: timedelta = None):
    payload = {"user_id": user_id}

    if expires_delta:
        payload["exp"] = datetime.now() + expires_delta

    token= jwt.encode(payload, os.environ["SECRET_KEY"],
        algorithm=os.environ["ALGORITHM"])
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def create_valid_token(user_id: int):
    return create_token(user_id)


def create_expired_token(user_id: int):
    return create_token(user_id, expires_delta=timedelta(seconds=-10))


def create_invalid_token():
    return create_token(9999)  # Assuming user_id 9999 does not exist
    #return "this.is.not.valid.jwt"


def create_token_with_wrong_secret(user_id: int):
    payload = {"user_id": user_id}
    return jwt.encode(payload, "wrong-secret", algorithm=ALGORITHM)