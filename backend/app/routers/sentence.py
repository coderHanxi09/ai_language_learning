from fastapi import APIRouter, HTTPException

from ..db import SessionLocal
from ..models_db import (
    ReadingSentenceDB,
    ReadingWordDB
)


router = APIRouter(
    prefix="/sentences",
    tags=["sentences"]
)



# =====================================================
# Get sentence detail
# =====================================================

@router.get("/{sentence_id}")
def get_sentence(sentence_id: int):

    session = SessionLocal()

    try:

        sentence = (
            session.query(
                ReadingSentenceDB
            )
            .filter(
                ReadingSentenceDB.id == sentence_id
            )
            .first()
        )


        if not sentence:

            raise HTTPException(
                status_code=404,
                detail="Sentence not found"
            )


        words = []

        for word in sentence.words:

            words.append(
                {
                    "id": word.id,
                    "word": word.word,
                    "lemma": word.lemma,
                    "position": word.position
                }
            )


        return {

            "id": sentence.id,

            "reading_id": sentence.reading_id,

            "order": sentence.sentence_order,

            "original": sentence.original,

            "translation": sentence.translation,

            "words": words

        }


    finally:

        session.close()





# =====================================================
# Get all sentences of one reading
# =====================================================

@router.get("/reading/{reading_id}")
def get_reading_sentences(
    reading_id: int
):


    session = SessionLocal()


    try:


        sentences = (

            session.query(
                ReadingSentenceDB
            )

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



        result = []



        for sentence in sentences:


            words = []

            for word in sentence.words:

                words.append(

                    {
                        "id": word.id,

                        "word": word.word,

                        "lemma": word.lemma,

                        "position": word.position
                    }

                )


            result.append(

                {

                    "id": sentence.id,

                    "order": sentence.sentence_order,

                    "original": sentence.original,

                    "translation": sentence.translation,

                    "words": words

                }

            )


        return result



    finally:

        session.close()