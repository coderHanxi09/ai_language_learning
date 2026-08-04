from fastapi import APIRouter, HTTPException

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


    result = lookup_word(
        word
    )


    if not result:

        raise HTTPException(

            status_code=404,

            detail="Word not found"

        )


    return result