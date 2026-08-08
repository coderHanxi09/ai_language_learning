from fastapi import APIRouter, HTTPException


from ..services.dictionary_service import (
    lookup_word
)



router = APIRouter()






# =====================================================
# GET dictionary word
# =====================================================

@router.get("/{word}")
def get_dictionary_word(
    word: str,
    language: str = "de"
):


    # =========================
    # Normalize input
    # =========================

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





    # =========================
    # Lookup
    # =========================

    result = lookup_word(

        normalized_word,

        language

    )





    # =========================
    # Not found
    # =========================

    if not result:


        return {


            "word":
                normalized_word,


            "found":
                False,


            "message":
                "Word not found"

        }






    # =========================
    # Success
    # =========================

    return {


        "word":
            normalized_word,


        "found":
            True,


        "data":
            result

    }