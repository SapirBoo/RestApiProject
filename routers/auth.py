from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

import db
from fastapi import FastAPI, HTTPException ,APIRouter,status,Depends
from sqlalchemy.orm import Session
from models.user import User
from resources.user import send_email
from schemas.user import UserResponse,UserCreate,UserLogin
from utils.security import hash_password, verify_password
from db import get_db
from utils.jwt import create_access_token,create_refresh_token,SECRET_KEY,ALGORITHM
from dependencies.auth import security,decode_and_validate_token

import jwt

from dependencies.auth import blacklist, get_current_user

rt=APIRouter(tags=["auth"])


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("jti") in blacklist:
            raise HTTPException(status_code=401, detail="Token revoked")

        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


# ---- Register ----
@rt.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    existing = db.query(User).filter(User.email == user.email).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="User with this email is allredy exists")
    
    new_user = User(
        username=user.username,
        email=user.email,
        content="This is a test email",
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    send_email(to_email=user.email,subject="You register successfully! ")
    
    return {"msg": "User created successfully"}

# ---- Login ----
@rt.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()

    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})
    
    return {
        "access_token": access_token,
        "refresh_token":refresh_token,
        "token_type": "bearer"
    }
    
# ---- Logout ----
@rt.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    payload=decode_and_validate_token(token,expected_type="access")
    
    blacklist.add(payload.get("jti"))

    return {"msg": "Logged out successfully"}

    
# ---- Protected ----
@rt.get("/protected")
def protected(current_user: User = Depends(get_current_user)):
    return {
        "msg": "You are authorized",
        "user": current_user.username
    }
    
@rt.post("/refresh")
def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials 
    payload = decode_and_validate_token(token,expected_type="refresh") 

    user_name = payload.get("sub")
    user=db.query(User).filter(User.username== user_name).first()
    
    if not user :
        raise HTTPException(status_code=401, detail="User not found")

    blacklist.add(payload.get("jti"))  # invalidate old refresh

    new_access_token = create_access_token({"sub": user_name})
    new_refresh_token = create_refresh_token({"sub": user_name})
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }