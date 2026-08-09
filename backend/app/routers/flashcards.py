from fastapi import (
    APIRouter,
    HTTPException,
    Query
)

from pydantic import BaseModel

from ..db import SessionLocal

from ..models_db import (
    FlashcardDB
)


router = APIRouter()







# =====================================================
# Request Models
# =====================================================

class FlashcardUpdateRequest(BaseModel):

    status: str







# =====================================================
# GET /flashcards
# =====================================================

@router.get("")
def get_flashcards(

    set_number: int = Query(
        default=1
    ),

    language: str = Query(
        default="de"
    )

):


    session = SessionLocal()



    try:


        cards = session.query(

            FlashcardDB

        ).join(

            FlashcardDB.vocabulary

        ).filter(


            FlashcardDB.set_number
            ==
            set_number,


            FlashcardDB.vocabulary.has(

                source_language=language

            )


        ).order_by(

            FlashcardDB.created_at.asc()

        ).all()






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


                "set_number":
                    card.set_number,


                "vocabulary_id":
                    card.vocabulary_id,


                "source_language":
                    card.vocabulary.source_language


            }


            for card in cards


        ]



    finally:


        session.close()







# =====================================================
# GET /flashcards/sets
# =====================================================

@router.get("/sets")
def get_flashcard_sets(

    language: str = Query(
        default="de"
    )

):


    session = SessionLocal()



    try:


        result = session.query(

            FlashcardDB.set_number

        ).join(

            FlashcardDB.vocabulary

        ).filter(

            FlashcardDB.vocabulary.has(

                source_language=language

            )

        ).distinct().order_by(

            FlashcardDB.set_number.asc()

        ).all()





        return [


            {


                "set_number":
                    item[0]


            }


            for item in result


        ]



    finally:


        session.close()







# =====================================================
# PUT /flashcards/{id}
# =====================================================

@router.put("/{flashcard_id}")
def update_flashcard(

    flashcard_id:int,

    req:FlashcardUpdateRequest

):


    session = SessionLocal()



    try:


        card = session.query(

            FlashcardDB

        ).filter(

            FlashcardDB.id
            ==
            flashcard_id

        ).first()




        if not card:


            raise HTTPException(

                status_code=404,

                detail="Flashcard not found"

            )






        card.status = req.status



        session.commit()



        return {


            "id":
                card.id,


            "status":
                card.status


        }




    finally:


        session.close()







# =====================================================
# DELETE
# =====================================================

@router.delete("/{flashcard_id}")
def delete_flashcard(

    flashcard_id:int

):


    session = SessionLocal()



    try:


        card = session.query(

            FlashcardDB

        ).filter(

            FlashcardDB.id
            ==
            flashcard_id

        ).first()




        if not card:


            raise HTTPException(

                status_code=404,

                detail="Flashcard not found"

            )




        session.delete(card)


        session.commit()



        return {


            "message":
                "deleted"

        }



    finally:


        session.close()