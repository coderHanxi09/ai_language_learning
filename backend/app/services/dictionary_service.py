from typing import Optional
import json
from ..db import SessionLocal
from ..models_db import DictionaryEntryDB


_MOCK_DB = {
    "serendipity": {
        "lemma": "serendipity",
        "definition": "the occurrence of events by chance in a happy or beneficial way",
        "pos": "noun",
        "cefr": "C1",
        "ipa": "/ˌsɛrənˈdɪpɪti/",
        "examples": ["Finding the manuscript was pure serendipity."],
    },
    "apple": {
        "lemma": "apple",
        "definition": "a round fruit with red or green skin",
        "pos": "noun",
        "cefr": "A1",
        "ipa": "/ˈæpəl/",
        "examples": ["She ate an apple for breakfast."],
    },
}


def _row_to_entry(row: DictionaryEntryDB) -> dict:
    if row is None:
        return None
    examples = []
    try:
        examples = json.loads(row.examples) if row.examples else []
    except Exception:
        examples = row.examples.split("\n") if row.examples else []
    return {
        "lemma": row.lemma or row.word,
        "definition": row.definition,
        "pos": row.pos,
        "cefr": row.cefr,
        "ipa": row.ipa,
        "examples": examples,
    }


def lookup_word(word: str) -> Optional[dict]:
    # Try DB first
    session = SessionLocal()
    try:
        row = session.query(DictionaryEntryDB).filter(DictionaryEntryDB.word == word.lower()).first()
        if row:
            return _row_to_entry(row)
    finally:
        session.close()

    # Fallback to mock
    return _MOCK_DB.get(word.lower())

