from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse
from auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

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