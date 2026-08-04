from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..db import SessionLocal
from ..models_db import FlashcardDB

router = APIRouter()


class FlashcardCreate(BaseModel):
    front: str
    back: str
    vocabulary_id: int | None = None


@router.post("/")
def create_flashcard(body: FlashcardCreate):
    session = SessionLocal()
    try:
        f = FlashcardDB(front=body.front, back=body.back, vocabulary_id=body.vocabulary_id)
        session.add(f)
        session.commit()
        session.refresh(f)
        return {"id": f.id, "front": f.front}
    finally:
        session.close()


@router.get("/")
def list_flashcards():
    session = SessionLocal()
    try:
        rows = session.query(FlashcardDB).all()
        return [{"id": r.id, "front": r.front, "back": r.back, "status": r.status} for r in rows]
    finally:
        session.close()
