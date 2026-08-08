import json
from typing import Optional, List


from ..db import SessionLocal

from ..models_db import (
    DictionaryEntryDB,
    DictionaryTranslationDB
)

from .word_token_service import normalize_word

from ..ai.factory import get_ai_provider





# =====================================================
# Helpers
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

    except:

        return []







def _normalize_language(
    language:str
):

    if not language:

        return "de"



    language = language.lower()



    mapping = {

        "german":"de",

        "deutsch":"de",

        "english":"en",

        "englisch":"en"

    }



    return mapping.get(

        language,

        language

    )







# =====================================================
# Database lookup
# =====================================================


def _database_lookup(
    word:str,
    language:str
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





        translations={}



        for t in entry.translations:


            translations[
                t.language
            ] = t.translation






        return {


            "id":
                entry.id,


            "word":
                entry.word,


            "lemma":
                entry.lemma,


            "language":
                entry.language,


            "definition":
                entry.definition,


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
# AI dictionary generation
# =====================================================


def _generate_with_ai(
    word:str,
    language:str
):


    provider = get_ai_provider()



    prompt = f"""

You are a professional dictionary.

Create a dictionary entry for:

Word:
{word}

Language:
{language}


Return ONLY valid JSON:

{{
 "word":"",
 "lemma":"",
 "definition":"",
 "translation":"",
 "pos":"",
 "cefr":"",
 "ipa":"",
 "examples":[]
}}

Rules:

- definition must be in English
- translation must be English
- CEFR level A1-C2
- For German words provide German lemma
- Provide one example sentence

"""



    result = provider.generate(
        prompt
    )



    try:

        data=json.loads(
            result
        )

    except Exception:


        return None




    return {


        "word":
            data.get(
                "word",
                word
            ),


        "lemma":
            data.get(
                "lemma",
                word
            ),


        "language":
            language,


        "definition":
            data.get(
                "definition"
            ),


        "pos":
            data.get(
                "pos"
            ),


        "cefr":
            data.get(
                "cefr"
            ),


        "ipa":
            data.get(
                "ipa"
            ),


        "examples":
            data.get(
                "examples",
                []
            ),


        "translations":

            {

                "en":

                data.get(
                    "translation"
                )

            }


    }







# =====================================================
# Save dictionary
# =====================================================


def _save_dictionary_entry(
    data:dict
):


    session=SessionLocal()



    try:


        existing=session.query(

            DictionaryEntryDB

        ).filter(

            DictionaryEntryDB.lemma ==
            data["lemma"],


            DictionaryEntryDB.language ==
            data["language"]

        ).first()



        if existing:

            return existing.id





        entry=DictionaryEntryDB(


            word=data["word"],


            lemma=data["lemma"],


            language=data["language"],


            definition=data.get(
                "definition"
            ),


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



        session.add(entry)


        session.flush()






        for lang,text in data.get(

            "translations",

            {}

        ).items():



            if text:


                session.add(

                    DictionaryTranslationDB(

                        dictionary_id=entry.id,

                        language=lang,

                        translation=text

                    )

                )





        session.commit()



        return entry.id




    finally:


        session.close()







# =====================================================
# Main lookup
# =====================================================


def lookup_word(
    word:str,
    language:str="de"
):


    language=_normalize_language(
        language
    )


    if not word:

        return None



    word=word.strip()



    # normalize lemma

    try:

        lemma=normalize_word(

            word,

            language

        )

    except:

        lemma=word.lower()





    # 1. database

    result=_database_lookup(

        lemma,

        language

    )



    if result:

        return result





    # 2. AI generation

    result=_generate_with_ai(

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


        item=lookup_word(

            word,

            language

        )


        if item:


            result[word]=item



    return result