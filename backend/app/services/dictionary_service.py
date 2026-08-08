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
                json.loads(entry.examples)
                if entry.examples
                else [],


            "translations":
                translations

        }



    finally:

        session.close()







# =====================================================
# Gemini dictionary lookup
# =====================================================

def _ai_dictionary_lookup(
    word: str,
    language: str
):


    provider = get_ai_provider()



    prompt = f"""
You are a professional dictionary.

Create a dictionary entry.

Word:
{word}

Language:
{language}


Return ONLY valid JSON.

Format:

{{
 "word":"",
 "lemma":"",
 "language":"",
 "pos":"",
 "cefr":"",
 "ipa":"",
 "examples":[],
 "translations": {{
     "en":""
 }},
 "definition":""
}}

Requirements:

- If German word, explain German meaning.
- Provide English translation.
- Provide CEFR level.
- Provide IPA if possible.
- Examples must be in original language.
"""



    response = provider.generate(
        prompt
    )



    try:


        data = json.loads(
            response
        )


        return data



    except Exception as e:


        print(
            "[DICTIONARY AI ERROR]",
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
    data:dict
):


    session = SessionLocal()


    try:


        exists = session.query(
            DictionaryEntryDB
        ).filter(
            DictionaryEntryDB.word == data["word"],
            DictionaryEntryDB.language == data["language"]
        ).first()



        if exists:

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



        for lang, text in data.get(
            "translations",
            {}
        ).items():


            session.add(

                DictionaryTranslationDB(

                    dictionary_id=entry.id,


                    language=lang,


                    translation=text

                )

            )



        session.commit()



    except Exception:


        session.rollback()

        raise



    finally:

        session.close()







# =====================================================
# Public lookup
# =====================================================

def lookup_word(
    word:str,
    language:str="de"
):


    word = word.strip().lower()



    # 1. database

    result = _database_lookup(
        word,
        language
    )


    if result:

        return result





    # 2. AI dictionary

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
# Batch
# =====================================================

def lookup_words(
    words:List[str],
    language:str="de"
):


    result={}



    for word in words:


        data = lookup_word(
            word,
            language
        )


        if data:

            result[word]=data



    return result