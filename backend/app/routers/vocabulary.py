from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

from ..db import SessionLocal

from ..models_db import (
    VocabularyDB,
    DictionaryEntryDB,
    VocabularyTranslationDB
)


router = APIRouter()



# =========================
# Request Model
# =========================

class VocabularyCreate(BaseModel):

    word: str

    lemma: str

    source_language: str = "de"

    definition: str | None = None

    cefr: str | None = None

    ipa: str | None = None

    translation: str | None = None





# =========================
# Add vocabulary
# POST /vocabulary
# =========================

@router.post("")
def add_vocabulary(
    req: VocabularyCreate
):


    session = SessionLocal()


    try:


        existing = session.query(
            VocabularyDB
        ).filter(
            VocabularyDB.lemma == req.lemma,
            VocabularyDB.source_language == req.source_language
        ).first()



        if existing:

            return {

                "message":
                    "Already exists",

                "id":
                    existing.id

            }




        vocab = VocabularyDB(

            word=req.word,

            lemma=req.lemma,

            source_language=req.source_language,

            definition=req.definition,

            cefr=req.cefr,

            ipa=req.ipa,

            source="reading"

        )


        session.add(vocab)


        session.flush()



        if req.translation:


            translation = VocabularyTranslationDB(

                vocabulary_id=vocab.id,

                language="en",

                translation=req.translation

            )


            session.add(
                translation
            )



        session.commit()


        session.refresh(
            vocab
        )



        return {

            "id": vocab.id,

            "word": vocab.word,

            "lemma": vocab.lemma

        }



    except Exception as e:


        session.rollback()

        raise e



    finally:

        session.close()





# =========================
# GET vocabulary
# =========================

@router.get("")
def get_vocabulary():


    session = SessionLocal()


    try:


        words = session.query(
            VocabularyDB
        ).all()



        return [

            {

                "id": w.id,

                "word": w.word,

                "lemma": w.lemma,

                "definition": w.definition,

                "cefr": w.cefr,

                "language": w.source_language

            }

            for w in words

        ]


    finally:

        session.close()