from app.db import SessionLocal

from app.models_db import (
    ReadingDB,
    ReadingSentenceDB,
)

from app.services.sentence_service import (
    split_sentences
)




def sync_reading_sentences():

    session = SessionLocal()


    try:

        readings = session.query(
            ReadingDB
        ).all()


        inserted = 0



        for reading in readings:


            existing = session.query(
                ReadingSentenceDB
            ).filter(
                ReadingSentenceDB.reading_id == reading.id
            ).count()



            if existing > 0:

                continue



            sentences = split_sentences(
                reading.content
            )



            for index, sentence in enumerate(
                sentences
            ):


                obj = ReadingSentenceDB(

                    reading_id=reading.id,

                    sentence_order=index + 1,

                    original=sentence,

                    translation=None

                )


                session.add(obj)

                inserted += 1




        session.commit()


        print(
            f"Inserted {inserted} sentences"
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

    sync_reading_sentences()