import json
from typing import Optional, List


from ..db import SessionLocal

from ..models_db import (
    DictionaryEntryDB,
    DictionaryTranslationDB
)





# =====================================================
# Parse examples
# =====================================================

def _parse_examples(
    examples
):

    if not examples:
        return []


    if isinstance(
        examples,
        list
    ):
        return examples


    try:
        return json.loads(
            examples
        )

    except Exception:
        return []







# =====================================================
# Normalize language
# =====================================================

def _normalize_language(
    language: str
):

    if not language:
        return "de"


    language = language.lower()


    if language in [
        "german",
        "deutsch"
    ]:
        return "de"


    if language in [
        "english",
        "englisch"
    ]:
        return "en"


    return language






# =====================================================
# Database lookup
# =====================================================

def _database_lookup(
    word: str,
    language: str
):


    session = SessionLocal()


    try:

        entry = session.query(
            DictionaryEntryDB
        ).filter(
            DictionaryEntryDB.lemma.ilike(word),
            DictionaryEntryDB.language == language
        ).first()



        if not entry:


            entry = session.query(
                DictionaryEntryDB
            ).filter(
                DictionaryEntryDB.word.ilike(word),
                DictionaryEntryDB.language == language
            ).first()



        if not entry:

            return None




        translations = {}


        for t in entry.translations:

            translations[
                t.language
            ] = t.translation





        return {


            "word":
                entry.word,


            "lemma":
                entry.lemma,


            "language":
                entry.language,


            "pos":
                entry.pos,


            "cefr":
                entry.cefr,


            "ipa":
                entry.ipa,


            "examples":
                _parse_examples(
                    entry.examples
                ),


            "translations":
                translations

        }



    finally:

        session.close()







# =====================================================
# German fallback dictionary
# =====================================================

def _german_fallback(
    word: str
):

    """
    Temporary fallback.

    Later can replace with:
    - Wiktionary API
    - DWDS API
    - dict.cc API
    - LLM dictionary generation
    """



    common_words = {


        "technologie": {

            "translation":
                "technology",

            "pos":
                "noun",

            "cefr":
                "B1"

        },


        "innovation": {

            "translation":
                "innovation",

            "pos":
                "noun",

            "cefr":
                "B2"

        },


        "entwicklung": {

            "translation":
                "development",

            "pos":
                "noun",

            "cefr":
                "B2"

        },


        "entscheidung": {

            "translation":
                "decision",

            "pos":
                "noun",

            "cefr":
                "B2"

        }


    }



    data = common_words.get(
        word.lower()
    )



    if not data:

        return None




    return {


        "word":
            word,


        "lemma":
            word,


        "language":
            "de",


        "pos":
            data["pos"],


        "cefr":
            data["cefr"],


        "ipa":
            None,


        "examples":
            [],


        "translations":

            {

                "en":
                    data["translation"]

            }

    }







# =====================================================
# Save dictionary entry
# =====================================================

def _save_dictionary_entry(
    data: dict
):


    session = SessionLocal()


    try:


        existing = session.query(
            DictionaryEntryDB
        ).filter(
            DictionaryEntryDB.lemma == data["lemma"],
            DictionaryEntryDB.language == data["language"]
        ).first()



        if existing:

            return existing.id




        entry = DictionaryEntryDB(

            word=data["word"],

            lemma=data["lemma"],

            language=data["language"],

            pos=data.get(
                "pos"
            ),

            cefr=data.get(
                "cefr"
            ),

            ipa=data.get(
                "ipa"
            ),

            examples=json.dumps(
                data.get(
                    "examples",
                    []
                ),
                ensure_ascii=False
            )

        )



        session.add(
            entry
        )


        session.flush()



        translations = data.get(
            "translations",
            {}
        )



        for lang, text in translations.items():


            translation = DictionaryTranslationDB(

                dictionary_id=entry.id,

                language=lang,

                translation=text

            )


            session.add(
                translation
            )



        session.commit()



        return entry.id



    except Exception:


        session.rollback()

        raise



    finally:

        session.close()







# =====================================================
# Single word lookup
# =====================================================

def lookup_word(
    word: str,
    language: str = "de"
) -> Optional[dict]:


    word = word.strip()


    if not word:

        return None



    language = _normalize_language(
        language
    )



    # 1. database

    result = _database_lookup(
        word,
        language
    )



    if result:

        return result





    # 2. fallback

    if language == "de":


        result = _german_fallback(
            word
        )



        if result:


            _save_dictionary_entry(
                result
            )


            return result





    return None







# =====================================================
# Batch lookup
# =====================================================

def lookup_words(
    words: List[str],
    language: str = "de"
):


    result = {}



    for word in words:


        data = lookup_word(
            word,
            language
        )


        if data:

            result[word] = data



    return result