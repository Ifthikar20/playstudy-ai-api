# routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse, UserLogin
from auth import get_current_user, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    # Create new user with generated ID and hashed password
    user_id = str(uuid.uuid4())
    db_user = User(
        id=user_id,
        email=user_data.email,
        password_hash=generate_password_hash(user_data.password),
        name=user_data.name,
        image=user_data.image
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Remove password_hash from response
    response_user = UserResponse(
        id=db_user.id,
        email=db_user.email,
        name=db_user.name,
        image=db_user.image,
        created_at=db_user.created_at
    )
    
    return response_user

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Find user by email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Verify user exists and password is correct
    if not user or not check_password_hash(user.password_hash, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate JWT token
    token_data = {
        "user_id": user.id,
        "email": user.email,
        "name": user.name,
        "image": user.image
    }
    access_token = create_access_token(token_data)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == current_user["user_id"]).first()

    if db_user is None:
        print(f"👤 User not found in DB. Auto-creating user: {current_user['email']}")
        db_user = User(
            id=current_user["user_id"],
            email=current_user["email"],
            name=current_user["name"],
            image=current_user["image"],
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    return db_user
