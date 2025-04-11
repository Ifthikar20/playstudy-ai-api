from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Score
from schemas import ScoreCreate, ScoreResponse
from auth import get_current_user

router = APIRouter(prefix="/scores", tags=["scores"])

@router.post("/", response_model=ScoreResponse)
async def create_score(score_data: ScoreCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_score = Score(
        user_id=current_user["user_id"],
        game_id=score_data.game_id,
        score=score_data.score
    )
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score

@router.get("/", response_model=list[ScoreResponse])
async def get_scores(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    scores = db.query(Score).filter(Score.user_id == current_user["user_id"]).all()
    return scores