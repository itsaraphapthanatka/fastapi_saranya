from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.users import Users
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    return users

class userCreate(BaseModel):
    username: str
    password: str
    email: str
    status: str
    createuser: Optional[str] = None
    createdate: Optional[datetime] = None

@router.post("/")
def create_user(
    user: userCreate,
    db: Session = Depends(get_db)
    ):
    new_user = Users(
        uname=user.username,
        upass=user.password,
        email=user.email,
        ustatus=user.status,
        createuser=user.createuser,
        createdate=user.createdate or datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}")
def update_user(
    user_id: int,
    user: userCreate,
    db: Session = Depends(get_db)
    ):
    existing_user = db.query(Users).filter(Users.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_user.uname = user.username
    existing_user.upass = user.password
    existing_user.email = user.email
    existing_user.ustatus = user.status
    existing_user.createdate = user.createdate or existing_user.createdate
    
    db.commit()
    db.refresh(existing_user)
    return existing_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

@router.post("/login")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == email, Users.upass == password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"detail": "Login successful", "user_id": user.id}