from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Note
from schemas import NoteCreate, NoteResponse
from auth import get_current_user

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=NoteResponse)
async def create_note(note_data: NoteCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_note = Note(
        user_id=current_user["user_id"],
        title=note_data.title,
        content=note_data.content
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/", response_model=list[NoteResponse])
async def get_notes(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    notes = db.query(Note).filter(Note.user_id == current_user["user_id"]).all()
    return notes