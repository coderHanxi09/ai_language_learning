from pydantic import BaseModel
from typing import List, Optional


class DictionaryEntry(BaseModel):
    lemma: str
    definition: str
    pos: Optional[str]
    cefr: Optional[str]
    ipa: Optional[str]
    examples: Optional[List[str]]


class ReadingRequest(BaseModel):
    topic: str
    difficulty: str = "B2"
    known_vocabulary: List[str] = []


class ReadingResponse(BaseModel):
    title: str
    content: str
    vocabulary: List[str]
