from fastapi import APIRouter, HTTPException
from ..services.dictionary_service import lookup_word

router = APIRouter()


@router.get("/{word}")
def get_dictionary(word: str):
    entry = lookup_word(word)
    if entry is None:
        raise HTTPException(status_code=404, detail="word not found")
    return entry
