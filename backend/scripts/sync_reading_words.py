from app.db import SessionLocal

from app.models_db import (
    ReadingSentenceDB,
    ReadingWordDB,
)

from app.services.word_token_service import (
    tokenize_sentence,
    normalize_word,
)



def sync_reading_words():

    session = SessionLocal()

    try:

        sentences = session.query(
            ReadingSentenceDB
        ).all()


        inserted = 0


        for sentence in sentences:


            words = tokenize_sentence(
                sentence.original
            )


            for position, word in enumerate(
                words
            ):


                obj = ReadingWordDB(

                    sentence_id=sentence.id,

                    word=word,

                    lemma=normalize_word(
                        word
                    ),

                    position=position + 1

                )


                session.add(obj)

                inserted += 1



        session.commit()


        print(
            f"Inserted {inserted} words"
        )



    except Exception as e:

        session.rollback()

        print(
            "[ERROR]",
            e
        )

        raise



    finally:

        session.close()



if __name__ == "__main__":

    sync_reading_words()