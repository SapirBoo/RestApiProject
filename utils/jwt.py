from jose import jwt
from datetime import datetime, timedelta
import uuid

SECRET_KEY = "197607840771406874533202352549685804096"  # secrets.SystemRandom().getrandbits(128)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_token(data: dict, expires_delta: timedelta, token_type: str):
    to_encode = data.copy()
    to_encode.update({
        "exp": datetime.now() + expires_delta,
        "type": token_type,
        "jti": str(uuid.uuid4())  
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(data: dict):
    return create_token(
        data,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "access"
    )

def create_refresh_token(data: dict):
    return create_token(
        data,
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "refresh"
    )  
    
    
def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


    