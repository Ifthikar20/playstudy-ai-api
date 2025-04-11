from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    image: Optional[str] = None

class UserCreate(UserBase):
    id: str

class UserResponse(UserBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class ScoreCreate(BaseModel):
    game_id: str
    score: int

class ScoreResponse(BaseModel):
    id: int
    user_id: str
    game_id: str
    score: int
    created_at: datetime

    class Config:
        from_attributes = True

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteResponse(BaseModel):
    id: int
    user_id: str
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True