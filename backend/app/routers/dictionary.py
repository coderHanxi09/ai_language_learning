from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..services.dictionary_service import (
    lookup_word
)


router = APIRouter()



# =====================================================
# Request Model
# =====================================================

class DictionaryLookupRequest(BaseModel):

    word: str

    language: str = "de"




# =====================================================
# GET single word
# =====================================================

@router.get("/{word}")
def get_dictionary_word(
    word: str,
    language: str = "de"
):

    normalized_word = word.strip()


    result = lookup_word(
        normalized_word,
        language
    )


    if not result:

        return {

            "word": normalized_word,

            "language": language,

            "found": False,

            "message": "Word not found"

        }



    return {

        "word": normalized_word,

        "language": language,

        "found": True,

        "data": result

    }





# =====================================================
# POST lookup
# =====================================================

@router.post("/lookup")
def lookup_dictionary_word(
    body: DictionaryLookupRequest
):

    word = body.word.strip()


    result = lookup_word(
        word,
        body.language
    )


    if not result:

        return {

            "word": word,

            "language": body.language,

            "found": False

        }



    return {

        "word": word,

        "language": body.language,

        "found": True,

        "data": result

    }