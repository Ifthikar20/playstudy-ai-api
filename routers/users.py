from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse
from auth import get_current_user
from jose import jwt
from datetime import datetime, timedelta
import os  # Add this import

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Mock user validation (replace with real logic, e.g., Google OAuth)
    user = {
        "user_id": "test_user_123",
        "email": form_data.username,
        "name": "Test User",
        "image": None,
    }
    if form_data.password != "testpassword":  # Replace with real auth
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    
    # Generate JWT
    access_token_expires = timedelta(minutes=30)
    expire = datetime.utcnow() + access_token_expires
    to_encode = user.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("BACKEND_JWT_SECRET"), algorithm="HS256")
    return {"access_token": encoded_jwt, "token_type": "bearer"}

@router.post("/me", response_model=UserResponse)
async def create_or_get_user(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_data.id).first()
    if db_user:
        return db_user
    
    db_user = User(
        id=user_data.id,
        email=user_data.email,
        name=user_data.name,
        image=user_data.image
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=UserResponse)
async def get_user(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user