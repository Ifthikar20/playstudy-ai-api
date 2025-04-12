# auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

BACKEND_JWT_SECRET = os.getenv("BACKEND_JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Increased for better UX

# Use HTTPBearer instead of OAuth2PasswordBearer
oauth2_scheme = HTTPBearer()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Change this line
    encoded_jwt = jwt.encode(to_encode, BACKEND_JWT_SECRET, algorithm=ALGORITHM)  # Use 'algorithm' not 'algorithms'
    return encoded_jwt

# Decode token and extract user information
async def get_current_user(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, BACKEND_JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return {
            "user_id": user_id,
            "email": payload.get("email"),
            "name": payload.get("name"),
            "image": payload.get("image")
        }
    except JWTError:
        raise credentials_exception