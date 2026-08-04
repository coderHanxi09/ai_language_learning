from sqlalchemy import func

from ..db import SessionLocal
from ..models_db import DictionaryEntryDB

from .dictionary_service import lookup_word



# =========================
# Sync vocabulary
# =========================

def sync_vocabulary_to_dictionary(
    words: list[str]
):

    session = SessionLocal()


    try:

        for raw_word in words:


            if not raw_word:
                continue


            word = raw_word.lower().strip()



            if not word:
                continue



            # =========================
            # Check existing word
            # case insensitive
            # =========================

            exists = session.query(
                DictionaryEntryDB
            ).filter(
                func.lower(
                    DictionaryEntryDB.word
                )
                ==
                word
            ).first()



            if exists:

                print(
                    "[DICT] exists:",
                    word
                )

                continue



            # =========================
            # Lookup dictionary
            # =========================

            print(
                "[DICT] Looking up:",
                word
            )


            data = lookup_word(
                word
            )



            if not data:

                print(
                    "[DICT] No result:",
                    word
                )

                continue



            # =========================
            # Double check before insert
            # =========================

            duplicate = session.query(
                DictionaryEntryDB
            ).filter(
                func.lower(
                    DictionaryEntryDB.word
                )
                ==
                word
            ).first()



            if duplicate:

                print(
                    "[DICT] duplicate skipped:",
                    word
                )

                continue



            # =========================
            # Create entry
            # =========================

            entry = DictionaryEntryDB(

                word=word,

                lemma=data.get(
                    "lemma",
                    word
                ),

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

                examples=str(
                    data.get(
                        "examples",
                        []
                    )
                )

            )


            session.add(
                entry
            )


            # Important:
            # write immediately so following
            # duplicate words are detected

            session.flush()



            print(
                "[DICT] inserted:",
                word
            )



        session.commit()



    except Exception as e:

        session.rollback()

        print(
            "[DICT SYNC ERROR]",
            e
        )

        raise



    finally:

        session.close()