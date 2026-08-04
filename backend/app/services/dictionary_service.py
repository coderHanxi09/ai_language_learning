from pathlib import Path
import json

from ..db import SessionLocal
from ..models_db import DictionaryEntryDB


# =========================
# Dictionary file location
# =========================

BASE_DIR = Path(__file__).resolve().parents[2]


DICTIONARY_FILE = (
    BASE_DIR /
    "data" /
    "dictionary" /
    "test.jsonl"
)



# =========================
# Public API
# =========================

def lookup_word(word: str):

    """
    Lookup word.

    Priority:
    1. SQLite cache
    2. Local JSONL dictionary
    3. Save result to SQLite
    """


    word = word.lower().strip()


    session = SessionLocal()


    try:

        # =========================
        # 1. Search database cache
        # =========================

        existing = session.query(
            DictionaryEntryDB
        ).filter(
            DictionaryEntryDB.word == word
        ).first()



        if existing:


            return {

                "word": existing.word,

                "lemma": existing.lemma,

                "definition": existing.definition,

                "pos": existing.pos,

                "cefr": existing.cefr,

                "ipa": existing.ipa,

                "examples": (
                    json.loads(
                        existing.examples
                    )
                    if existing.examples
                    else []
                )

            }




        # =========================
        # 2. Search JSONL
        # =========================

        result = search_json_dictionary(
            word
        )



        if not result:

            return None




        # =========================
        # 3. Save cache
        # =========================

        entry = DictionaryEntryDB(

            word=result["word"],

            lemma=result.get(
                "lemma"
            ),

            definition=result.get(
                "definition"
            ),

            pos=result.get(
                "pos"
            ),

            cefr=result.get(
                "cefr"
            ),

            ipa=result.get(
                "ipa"
            ),

            examples=json.dumps(
                result.get(
                    "examples",
                    []
                )
            )

        )



        session.add(entry)

        session.commit()



        return result




    finally:

        session.close()







# =========================
# JSONL search
# =========================

def search_json_dictionary(
    word: str
):


    if not DICTIONARY_FILE.exists():

        print(
            "[Dictionary] File not found:",
            DICTIONARY_FILE
        )

        return None




    with open(
        DICTIONARY_FILE,
        "r",
        encoding="utf-8"
    ) as file:



        for line in file:


            if not line.strip():

                continue



            data = json.loads(
                line
            )



            if data.get(
                "word"
            ) != word:


                continue




            senses = data.get(
                "senses",
                []
            )



            definition = None



            if senses:


                glosses = senses[0].get(
                    "glosses",
                    []
                )


                if glosses:

                    definition = glosses[0]




            sounds = data.get(
                "sounds",
                []
            )



            ipa = None


            if sounds:

                ipa = sounds[0].get(
                    "ipa"
                )




            return {


                "word": word,


                "lemma": data.get(
                    "word"
                ),


                "definition": definition,


                "pos": data.get(
                    "pos"
                ),


                "cefr": data.get(
                    "cefr"
                ),


                "ipa": ipa,


                "examples": []

            }



    return None