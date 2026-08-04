from fastapi import APIRouter

from ..services.dictionary_service import (
    lookup_word
)


router = APIRouter()



# =========================
# Get dictionary entry
# =========================

@router.get("/{word}")
def get_dictionary_word(
    word: str
):


    normalized_word = word.lower().strip()



    result = lookup_word(
        normalized_word
    )



    if not result:


        return {

            "word": normalized_word,

            "found": False,

            "message": "Word not found"

        }



    return {

        "word": normalized_word,

        "found": True,

        "data": result

    }