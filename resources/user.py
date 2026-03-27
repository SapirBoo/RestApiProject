
import db
from fastapi import FastAPI, HTTPException ,APIRouter,status,Depends
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserResponse,UserCreate,UserLogin
from utils.security import hash_password

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