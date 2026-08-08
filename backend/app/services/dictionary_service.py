import json
import re
from typing import Optional, List


from ..db import SessionLocal

from ..models_db import (
    DictionaryEntryDB,
    DictionaryTranslationDB
)


from ..ai.factory import get_ai_provider





# =====================================================
# Helpers
# =====================================================


def _normalize_language(language: str):

    if not language:
        return "de"


    language = language.lower()


    mapping = {

        "german": "de",

        "deutsch": "de",

        "english": "en",

        "englisch": "en"

    }


    return mapping.get(
        language,
        language
    )





def _parse_json_response(text: str):

    """
    Extract JSON from AI response
    """


    try:

        return json.loads(text)


    except Exception:

        pass



    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )


    if match:

        try:

            return json.loads(
                match.group()
            )

        except Exception:

            return None



    return None







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

            DictionaryEntryDB.language == language,

            DictionaryEntryDB.lemma.ilike(word)

        ).first()



        if not entry:


            entry = session.query(
                DictionaryEntryDB
            ).filter(

                DictionaryEntryDB.language == language,

                DictionaryEntryDB.word.ilike(word)

            ).first()



        if not entry:

            return None





        translations = {}



        for item in entry.translations:


            translations[
                item.language
            ] = item.translation





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


            "definition":
                entry.definition,


            "examples":
                json.loads(
                    entry.examples
                )
                if entry.examples
                else [],



            "translation":

                translations.get(
                    "en"
                )

        }



    finally:

        session.close()







# =====================================================
# AI dictionary generation
# =====================================================


def _generate_dictionary(
    word: str,
    language: str
):


    provider = get_ai_provider()



    prompt = f"""

You are a professional dictionary.

Create a dictionary entry for this word:

Word:
{word}

Language:
{language}


Return ONLY JSON.

Format:

{{
 "word":"",
 "lemma":"",
 "language":"",
 "pos":"",
 "cefr":"",
 "ipa":"",
 "definition":"",
 "translation":"",
 "examples":[]
}}

Rules:

- definition must be in English
- translation must be English
- CEFR level should be A1-C2
- examples should be real sentences
- no markdown

"""



    response = provider.generate(
        prompt
    )



    data = _parse_json_response(
        response
    )



    if not data:

        return None



    return data







# =====================================================
# Save dictionary
# =====================================================


def _save_dictionary(
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


            definition=data.get(
                "definition"
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





        translation = data.get(
            "translation"
        )



        if translation:


            session.add(

                DictionaryTranslationDB(

                    dictionary_id=entry.id,

                    language="en",

                    translation=translation

                )

            )





        session.commit()



        return entry.id



    except Exception:


        session.rollback()

        raise



    finally:

        session.close()







# =====================================================
# Public lookup
# =====================================================


def lookup_word(
    word: str,
    language: str = "de"
):


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





    # 2. AI generate

    result = _generate_dictionary(

        word,

        language

    )



    if not result:

        return None





    _save_dictionary(
        result
    )



    return result







# =====================================================
# Batch lookup
# =====================================================


def lookup_words(
    words: List[str],
    language: str = "de"
):


    result = {}



    for word in words:


        item = lookup_word(

            word,

            language

        )


        if item:

            result[word] = item



    return result