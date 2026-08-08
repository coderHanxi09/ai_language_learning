from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..db import SessionLocal

from ..models_db import (
    FlashcardDB,
    VocabularyDB,
    VocabularyTranslationDB
)


router = APIRouter()





# =====================================================
# Request Models
# =====================================================


class FlashcardCreate(BaseModel):

    vocabulary_id: int | None = None

    front: str | None = None

    back: str | None = None






# =====================================================
# Create Flashcard
# =====================================================


@router.post("")
def create_flashcard(
    body: FlashcardCreate
):


    session = SessionLocal()


    try:


        front = body.front

        back = body.back



        # =================================================
        # Create from vocabulary
        # =================================================

        if body.vocabulary_id:


            vocabulary = (

                session.query(
                    VocabularyDB
                )

                .filter(
                    VocabularyDB.id
                    ==
                    body.vocabulary_id
                )

                .first()

            )


            if not vocabulary:


                raise HTTPException(

                    404,

                    "Vocabulary not found"

                )



            # duplicate check

            existing = (

                session.query(
                    FlashcardDB
                )

                .filter(
                    FlashcardDB.vocabulary_id
                    ==
                    vocabulary.id
                )

                .first()

            )


            if existing:


                return {

                    "message":
                        "already exists",

                    "id":
                        existing.id

                }




            front = vocabulary.word



            translation = (

                session.query(
                    VocabularyTranslationDB
                )

                .filter(
                    VocabularyTranslationDB.vocabulary_id
                    ==
                    vocabulary.id
                )

                .filter(
                    VocabularyTranslationDB.language
                    ==
                    "en"
                )

                .first()

            )



            if translation:

                back = translation.translation



            else:

                back = ""





        # =================================================
        # Manual creation
        # =================================================


        if not front:


            raise HTTPException(

                400,

                "front is required"

            )



        if back is None:

            back = ""




        card = FlashcardDB(

            front=front,

            back=back,

            vocabulary_id=
                body.vocabulary_id,

            status="learning"

        )


        session.add(
            card
        )


        session.commit()


        session.refresh(
            card
        )



        return {


            "message":
                "created",


            "id":
                card.id,


            "front":
                card.front,


            "back":
                card.back

        }



    finally:

        session.close()







# =====================================================
# Generate flashcard from vocabulary
# =====================================================


@router.post(
    "/from-vocabulary/{vocabulary_id}"
)
def create_from_vocabulary(
    vocabulary_id:int
):


    return create_flashcard(

        FlashcardCreate(

            vocabulary_id=vocabulary_id

        )

    )







# =====================================================
# Get all flashcards
# =====================================================


@router.get("")
def list_flashcards():


    session = SessionLocal()


    try:


        cards = (

            session.query(
                FlashcardDB
            )

            .order_by(
                FlashcardDB.id.desc()
            )

            .all()

        )



        return [

            {

                "id":
                    card.id,


                "front":
                    card.front,


                "back":
                    card.back,


                "status":
                    card.status,


                "vocabulary_id":
                    card.vocabulary_id

            }

            for card in cards

        ]



    finally:

        session.close()







# =====================================================
# Get one flashcard
# =====================================================


@router.get("/{card_id}")
def get_flashcard(
    card_id:int
):


    session = SessionLocal()


    try:


        card = (

            session.query(
                FlashcardDB
            )

            .filter(
                FlashcardDB.id
                ==
                card_id
            )

            .first()

        )


        if not card:


            raise HTTPException(

                404,

                "flashcard not found"

            )



        return {

            "id":
                card.id,

            "front":
                card.front,

            "back":
                card.back,

            "status":
                card.status,

            "vocabulary_id":
                card.vocabulary_id

        }



    finally:

        session.close()







# =====================================================
# Update learning status
# =====================================================


class FlashcardStatusUpdate(BaseModel):

    status: str






@router.patch("/{card_id}")
def update_status(
    card_id:int,
    body:FlashcardStatusUpdate
):


    session = SessionLocal()


    try:


        card = (

            session.query(
                FlashcardDB
            )

            .filter(
                FlashcardDB.id
                ==
                card_id
            )

            .first()

        )



        if not card:


            raise HTTPException(

                404,

                "flashcard not found"

            )



        card.status = body.status


        session.commit()



        return {

            "message":
                "updated",

            "status":
                card.status

        }



    finally:

        session.close()







# =====================================================
# Delete flashcard
# =====================================================


@router.delete("/{card_id}")
def delete_flashcard(
    card_id:int
):


    session = SessionLocal()


    try:


        card = (

            session.query(
                FlashcardDB
            )

            .filter(
                FlashcardDB.id
                ==
                card_id
            )

            .first()

        )



        if not card:


            raise HTTPException(

                404,

                "flashcard not found"

            )



        session.delete(
            card
        )


        session.commit()



        return {

            "message":
                "deleted"

        }



    finally:

        session.close()