
import db
from fastapi import FastAPI, HTTPException ,APIRouter,status,Depends
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserResponse,UserCreate,UserLogin
from utils.security import hash_password
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

rt=APIRouter(tags=["users"])

@rt.get("/user/{user_id}",status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(db.get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
            "id": user.id,
            "username":user.username
    }
            
@rt.delete("/user/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(db.get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()

def send_email(to_email: str, subject:str) :
    message= Mail(from_email=FROM_EMAIL,
                  to_emails=To(to_email),
                  subject=subject,
                  html_content="<h1>Welcome!</h1><p>Your account was created </p>"
                )
    try:
        sg=SendGridAPIClient(SENDGRID_API_KEY)
        response=sg.send(message)
        return {
            "status_code": response.status_code,
            "body": response.body.decode() if response.body else None,
        }
    except Exception as e:
        return {"error": str(e)}

@rt.get('/users', status_code=status.HTTP_200_OK)   
def get_all_users(db: Session = Depends(db.get_db)):  
    data=db.query(User).all()
    result = []
    for user in data:
        result.append({
            "id": user.id,
            "name": user.username,
            "email":user.email
        })

    return {
        "users": result,
        "total": len(result)
    }
   