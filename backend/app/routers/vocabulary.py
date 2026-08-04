from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..db import SessionLocal

from ..models_db import (
    VocabularyDB,
    ReadingWordDB,
    ReadingSentenceDB,
    FlashcardDB,
    DictionaryEntryDB
)


router = APIRouter()



# =========================
# Request Model
# =========================

class VocabCreate(BaseModel):

    word: str

    lemma: str | None = None

    definition: str | None = None

    cefr: str | None = None

    workspace_id: int | None = None




# =========================
# Manual add vocabulary
# =========================

@router.post("")
def create_vocab(
    body: VocabCreate
):

    session = SessionLocal()


    try:

        word = body.word.lower().strip()



        existing = session.query(
            VocabularyDB
        ).filter(
            VocabularyDB.word == word
        ).first()



        if existing:

            return {

                "message": "already exists",

                "id": existing.id,

                "word": existing.word

            }



        vocab = VocabularyDB(

            word=word,

            lemma=body.lemma,

            definition=body.definition,

            cefr=body.cefr,

            source="manual",

            workspace_id=body.workspace_id

        )


        session.add(vocab)

        session.commit()

        session.refresh(vocab)



        return {

            "message":"added",

            "id":vocab.id,

            "word":vocab.word

        }


    finally:

        session.close()




# =========================
# Add from reading
# =========================

@router.post("/from-reading")
def add_from_reading(
    body: dict
):


    word = body.get(
        "word"
    )


    reading_id = body.get(
        "reading_id"
    )



    if not word or not reading_id:

        raise HTTPException(

            status_code=400,

            detail="word and reading_id required"

        )



    session = SessionLocal()



    try:


        word = word.lower().strip()



        # =====================
        # Find word in reading
        # =====================

        reading_word = (

            session.query(
                ReadingWordDB
            )

            .join(
                ReadingSentenceDB
            )

            .filter(
                ReadingSentenceDB.reading_id == reading_id
            )

            .filter(
                ReadingWordDB.word == word
            )

            .first()

        )



        lemma = word



        if reading_word and reading_word.lemma:

            lemma = reading_word.lemma




        # =====================
        # Duplicate check
        # =====================

        existing = session.query(
            VocabularyDB
        ).filter(
            VocabularyDB.word == word
        ).first()



        if existing:

            return {

                "message":"already exists",

                "id":existing.id,

                "word":existing.word

            }




        # =====================
        # Dictionary lookup
        # =====================

        dictionary = session.query(
            DictionaryEntryDB
        ).filter(

            DictionaryEntryDB.word == lemma

        ).first()



        definition = None

        cefr = None



        if dictionary:

            definition = dictionary.definition

            cefr = dictionary.cefr




        # =====================
        # Create vocabulary
        # =====================

        vocab = VocabularyDB(

            word=word,

            lemma=lemma,

            definition=definition,

            cefr=cefr,

            source="reading",

            reading_id=reading_id

        )



        session.add(vocab)

        session.flush()




        # =====================
        # Create flashcard
        # =====================

        flashcard = FlashcardDB(

            front=word,

            back=definition or "",

            status="learning",

            vocabulary_id=vocab.id

        )


        session.add(flashcard)



        session.commit()



        session.refresh(
            vocab
        )



        return {

            "message":"added",

            "id":vocab.id,

            "word":vocab.word,

            "definition":definition,

            "cefr":cefr

        }



    finally:

        session.close()




# =========================
# Get all vocabulary
# =========================

@router.get("")
def get_vocabularies():

    session = SessionLocal()


    try:

        items = session.query(
            VocabularyDB
        ).order_by(
            VocabularyDB.id.desc()
        ).all()



        return [

            {

                "id":item.id,

                "word":item.word,

                "lemma":item.lemma,

                "definition":item.definition,

                "cefr":item.cefr,

                "source":item.source

            }

            for item in items

        ]


    finally:

        session.close()




# =========================
# Get one word
# =========================

@router.get("/{word}")
def get_vocab(
    word:str
):

    session = SessionLocal()



    try:

        vocab = session.query(
            VocabularyDB
        ).filter(

            VocabularyDB.word == word.lower()

        ).first()



        if not vocab:

            raise HTTPException(

                status_code=404,

                detail="vocabulary not found"

            )



        return {

            "id":vocab.id,

            "word":vocab.word,

            "lemma":vocab.lemma,

            "definition":vocab.definition,

            "cefr":vocab.cefr

        }



    finally:

        session.close()




# =========================
# Delete vocabulary
# =========================

@router.delete("/{word}")
def delete_vocab(
    word:str
):

    session = SessionLocal()



    try:

        vocab = session.query(
            VocabularyDB
        ).filter(

            VocabularyDB.word == word.lower()

        ).first()



        if not vocab:

            raise HTTPException(

                status_code=404,

                detail="vocabulary not found"

            )



        session.delete(
            vocab
        )

        session.commit()



        return {

            "message":"deleted",

            "word":word.lower()

        }



    finally:

        session.close()