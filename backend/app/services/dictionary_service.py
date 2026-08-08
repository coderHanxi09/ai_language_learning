import json
from typing import Optional, List


from app.ai.factory import get_ai_provider


from ..db import SessionLocal


from ..models_db import (
    DictionaryEntryDB,
    DictionaryTranslationDB
)





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
            DictionaryEntryDB.word.ilike(word),
            DictionaryEntryDB.language == language
        ).first()



        if not entry:


            entry = session.query(
                DictionaryEntryDB
            ).filter(
                DictionaryEntryDB.lemma.ilike(word),
                DictionaryEntryDB.language == language
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


            "definition":
                entry.definition,


            "cefr":
                entry.cefr,


            "ipa":
                entry.ipa,


            "examples":
                json.loads(
                    entry.examples
                )
                if entry.examples
                else [],


            "translations":
                translations

        }



    finally:

        session.close()







# =====================================================
# AI dictionary lookup
# =====================================================

def _ai_dictionary_lookup(
    word: str,
    language: str
):


    provider = get_ai_provider()



    prompt = f"""
You are a professional bilingual dictionary.

Create a dictionary entry.

Word:
{word}

Language:
{language}


Return ONLY JSON.

Format:

{{
    "word": "",
    "lemma": "",
    "language": "",
    "pos": "",
    "definition": "",
    "cefr": "",
    "ipa": "",
    "examples": [],
    "translations": {{
        "en": ""
    }}
}}


Requirements:

- Explain the meaning in English.
- Provide the original language examples.
- Provide CEFR level.
- Provide IPA if available.
- Keep the explanation concise.
"""



    response = provider.generate(
        prompt
    )



    try:


        return json.loads(
            response
        )



    except Exception as e:


        print(
            "[DICTIONARY JSON ERROR]",
            e
        )


        print(
            response
        )


        return None







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
            DictionaryEntryDB.word == data["word"],
            DictionaryEntryDB.language == data["language"]
        ).first()



        if existing:

            return





        entry = DictionaryEntryDB(


            word=data["word"],


            lemma=data.get(
                "lemma",
                data["word"]
            ),


            language=data["language"],


            pos=data.get(
                "pos"
            ),


            definition=data.get(
                "definition"
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



        for language, translation in translations.items():


            session.add(

                DictionaryTranslationDB(

                    dictionary_id=entry.id,


                    language=language,


                    translation=translation

                )

            )



        session.commit()



    except Exception as e:


        session.rollback()


        print(
            "[SAVE DICTIONARY ERROR]",
            e
        )


        raise



    finally:

        session.close()







# =====================================================
# Public API
# =====================================================

def lookup_word(
    word: str,
    language: str = "de"
) -> Optional[dict]:


    word = (
        word
        .strip()
        .lower()
    )



    if not word:

        return None





    # 1. database

    result = _database_lookup(

        word,

        language

    )



    if result:

        return result






    # 2. Gemini dictionary

    result = _ai_dictionary_lookup(

        word,

        language

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


        item = lookup_word(

            word,

            language

        )


        if item:

            result[word] = item



    return result