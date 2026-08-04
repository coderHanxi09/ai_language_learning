from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models_db import DictionaryEntryDB

from .dictionary_service import lookup_word




def sync_vocabulary_to_dictionary(
    vocabulary: list[str]
):

    """
    Sync generated reading vocabulary
    into dictionary_entries table.
    """

    session = SessionLocal()


    try:

        for word in vocabulary:


            # avoid duplicate

            exists = session.query(
                DictionaryEntryDB
            ).filter(
                DictionaryEntryDB.word == word.lower()
            ).first()


            if exists:

                continue



            print(
                f"[DICT] Looking up {word}"
            )



            data = lookup_word(
                word
            )



            if not data:

                print(
                    f"[DICT] No result for {word}"
                )

                continue



            entry = DictionaryEntryDB(

                word=data.get(
                    "word",
                    word.lower()
                ),


                lemma=data.get(
                    "lemma"
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



        session.commit()


        print(
            "[DICT] Vocabulary sync finished"
        )



    except Exception as e:


        print(
            "[DICT ERROR]",
            e
        )


        session.rollback()

        raise



    finally:

        session.close()