from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

from ..db import SessionLocal

from ..models_db import (
    VocabularyDB,
    VocabularyTranslationDB,
    FlashcardDB
)


router = APIRouter()







# =====================================================
# Request Model
# =====================================================

class VocabularyCreateRequest(BaseModel):

    word: str

    lemma: str

    source_language: str = "de"

    translation: str | None = None

    definition: str | None = None

    cefr: str | None = None

    ipa: str | None = None

    reading_id: int | None = None







# =====================================================
# Create Flashcard automatically
# =====================================================

def create_flashcard_for_vocabulary(
    session,
    vocabulary: VocabularyDB
):


    # check existing

    existing = session.query(
        FlashcardDB
    ).filter(

        FlashcardDB.vocabulary_id
        ==
        vocabulary.id

    ).first()



    if existing:

        return existing






    # count current flashcards

    count = session.query(
        FlashcardDB
    ).count()



    # every 100 words = new set

    set_number = (
        count // 100
    ) + 1






    # build back content

    back_parts = []



    if vocabulary.translations:


        for t in vocabulary.translations:


            back_parts.append(
                t.translation
            )



    if vocabulary.definition:


        back_parts.append(

            vocabulary.definition

        )



    if vocabulary.cefr:


        back_parts.append(

            f"CEFR: {vocabulary.cefr}"

        )



    if vocabulary.ipa:


        back_parts.append(

            f"IPA: {vocabulary.ipa}"

        )





    flashcard = FlashcardDB(


        front=vocabulary.word,


        back="\n".join(
            back_parts
        ),


        status="learning",


        set_number=set_number,


        vocabulary_id=vocabulary.id

    )



    session.add(
        flashcard
    )


    session.flush()



    return flashcard







# =====================================================
# POST /vocabulary
# =====================================================

@router.post("")
def create_vocabulary(
    req: VocabularyCreateRequest
):


    session = SessionLocal()



    try:


        # avoid duplicate

        existing = session.query(
            VocabularyDB
        ).filter(

            VocabularyDB.lemma == req.lemma,

            VocabularyDB.source_language
            ==
            req.source_language

        ).first()



        if existing:


            return {


                "id":
                    existing.id,


                "message":
                    "Vocabulary already exists"

            }







        vocabulary = VocabularyDB(


            word=req.word,


            lemma=req.lemma,


            source_language=req.source_language,


            definition=req.definition,


            cefr=req.cefr,


            ipa=req.ipa,


            reading_id=req.reading_id

        )



        session.add(
            vocabulary
        )


        session.flush()






        # save translation

        if req.translation:


            translation = VocabularyTranslationDB(


                vocabulary_id=vocabulary.id,


                language="en",


                translation=req.translation

            )


            session.add(
                translation
            )







        # create flashcard automatically

        flashcard = create_flashcard_for_vocabulary(

            session,

            vocabulary

        )







        session.commit()



        session.refresh(
            vocabulary
        )



        return {


            "id":
                vocabulary.id,


            "word":
                vocabulary.word,


            "flashcard_id":
                flashcard.id,


            "set_number":
                flashcard.set_number,


            "message":
                "Vocabulary and flashcard created"

        }





    except Exception as e:


        session.rollback()


        raise e



    finally:


        session.close()







# =====================================================
# GET /vocabulary
# =====================================================

@router.get("")
def get_vocabulary():


    session = SessionLocal()



    try:


        items = session.query(

            VocabularyDB

        ).order_by(

            VocabularyDB.id.desc()

        ).all()






        result = []



        for item in items:



            translation = None



            if item.translations:


                translation = (
                    item.translations[0]
                    .translation
                )




            result.append({


                "id":
                    item.id,


                "word":
                    item.word,


                "lemma":
                    item.lemma,


                "translation":
                    translation,


                "definition":
                    item.definition,


                "cefr":
                    item.cefr,


                "ipa":
                    item.ipa,


                "source_language":
                    item.source_language


            })




        return result




    finally:


        session.close()







# =====================================================
# DELETE
# =====================================================

@router.delete("/{vocabulary_id}")
def delete_vocabulary(
    vocabulary_id:int
):


    session = SessionLocal()



    try:


        item = session.query(
            VocabularyDB
        ).filter(

            VocabularyDB.id == vocabulary_id

        ).first()



        if not item:


            raise HTTPException(

                status_code=404,

                detail="Vocabulary not found"

            )



        session.delete(item)


        session.commit()



        return {


            "message":
                "deleted"

        }



    finally:


        session.close()