from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..db import SessionLocal
from ..models_db import VocabularyDB

router = APIRouter()


class VocabCreate(BaseModel):
    word: str
    lemma: str | None = None
    definition: str | None = None
    cefr: str | None = None
    workspace_id: int | None = None


@router.post("/")
def create_vocab(body: VocabCreate):
    session = SessionLocal()
    try:
        v = VocabularyDB(
            word=body.word.lower(),
            lemma=body.lemma,
            definition=body.definition,
            cefr=body.cefr,
            workspace_id=body.workspace_id,
        )
        session.add(v)
        session.commit()
        session.refresh(v)
        return {"id": v.id, "word": v.word}
    finally:
        session.close()


@router.get("/{word}")
def get_vocab(word: str):
    session = SessionLocal()
    try:
        v = session.query(VocabularyDB).filter(VocabularyDB.word == word.lower()).first()
        if not v:
            raise HTTPException(status_code=404, detail="vocabulary not found")
        return {"id": v.id, "word": v.word, "definition": v.definition, "cefr": v.cefr}
    finally:
        session.close()
