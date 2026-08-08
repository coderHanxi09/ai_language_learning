from fastapi import APIRouter, HTTPException

from ..services.dictionary_service import (
    lookup_word
)


router = APIRouter()





# =====================================================
# GET dictionary word
# GET /dictionary/{word}?language=de
# =====================================================


@router.get("/{word}")
def get_dictionary_word(
    word: str,
    language: str = "de"
):


    normalized_word = (
        word
        .strip()
        .lower()
    )



    if not normalized_word:


        raise HTTPException(

            status_code=400,

            detail="Word cannot be empty"

        )





    result = lookup_word(

        normalized_word,

        language

    )





    if not result:


        return {


            "word":
                normalized_word,


            "found":
                False,


            "message":
                "Word not found"


        }






    return {


        "word":
            normalized_word,


        "found":
            True,


        "data":
            result


    }