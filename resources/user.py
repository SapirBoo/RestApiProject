
import db
from fastapi import FastAPI, HTTPException ,APIRouter,status,Depends
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserResponse,UserCreate,UserLogin
from utils.security import hash_password
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

rt=APIRouter(tags=["users"])

@rt.get("/user/{user_id}",status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(db.get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
            "id": user.id,
            "username":user.username
    }
            
@rt.delete("/user/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(db.get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()

def send_email(to_email: str, subject:str) :
    message= Mail(from_email=FROM_EMAIL,
                  to_emails=to_email,
                  subject=subject,
                  content="<h1>Welcome!</h1><p>Your account was created </p>",
                  html_content=content)
    try:
        sg=SendGridAPIClient(SENDGRID_API_KEY)
        response=sg.send(message)
        return {
            "status_code": response.status_code,
            "body": response.body.decode() if response.body else None,
        }
    except Exception as e:
        return {"error": str(e)}
    
    
        