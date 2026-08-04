from fastapi import APIRouter, HTTPException

from ..db import SessionLocal
from ..models_db import ReadingSentenceDB

router = APIRouter()


@router.get("/readings/{reading_id}/sentences")
def get_sentences(reading_id: int):
    """
    Get all sentences for one reading.
    """

    session = SessionLocal()

    try:

        sentences = (
            session.query(ReadingSentenceDB)
            .filter(
                ReadingSentenceDB.reading_id == reading_id
            )
            .order_by(
                ReadingSentenceDB.sentence_order
            )
            .all()
        )

        if not sentences:
            raise HTTPException(
                status_code=404,
                detail="No sentences found"
            )

        return [
            {
                "id": s.id,
                "order": s.sentence_order,
                "original": s.original,
                "translation": s.translation
            }
            for s in sentences
        ]

    finally:
        session.close()