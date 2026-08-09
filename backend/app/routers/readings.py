from fastapi import (
    APIRouter,
    HTTPException,
    BackgroundTasks
)

from pydantic import BaseModel

import json


from ..db import SessionLocal


from ..models_db import (
    ReadingDB,
    ReadingSentenceDB,
    ReadingWordDB
)


from ..services.sentence_service import (
    split_sentences
)


from ..services.translation_service import (
    translate_sentences
)


from ..services.word_token_service import (
    analyze_sentence
)


from ..ai.factory import get_ai_provider



router = APIRouter()







# =====================================================
# Request
# =====================================================

class ReadingRequest(BaseModel):

    title: str | None = None

    content: str

    source_language: str = "de"

    translation_language: str = "en"

    difficulty: str = "B2"









# =====================================================
# Create DB record
# =====================================================


def create_reading(payload:dict):


    session = SessionLocal()


    try:


        reading = ReadingDB(

            title=
                payload.get("title")
                or
                "Generating title...",


            content=
                payload["content"],


            difficulty=
                payload.get(
                    "difficulty",
                    "B2"
                ),


            source_language=
                payload.get(
                    "source_language",
                    "de"
                ),


            translation_language=
                payload.get(
                    "translation_language",
                    "en"
                ),


            vocabulary=json.dumps([]),


            status="processing"

        )


        session.add(reading)

        session.commit()

        session.refresh(reading)


        return reading.id


    finally:

        session.close()







# =====================================================
# Generate title
# =====================================================


def generate_title(content, language):


    try:


        provider=get_ai_provider()



        prompt=f"""

Generate a short title.

Language:
{language}

Maximum 8 words.

Return only title.

Text:

{content[:1500]}

"""


        result=provider.generate(
            prompt
        ).strip()


        if result:

            return result



    except Exception as e:


        print(
            "[TITLE ERROR]",
            e
        )


    return "Imported Reading"









# =====================================================
# Save sentences
# =====================================================


def save_sentences(
    session,
    reading_id,
    content,
    source_language,
    translation_language
):


    sentences = split_sentences(
        content
    )


    translations = translate_sentences(
        sentences,
        source_language,
        translation_language
    )



    translation_map={}



    for item in translations:

        translation_map[
            item["sentence_order"]
        ] = item["translation"]







    for index,sentence in enumerate(sentences):


        sentence_db = ReadingSentenceDB(

            reading_id=
                reading_id,


            sentence_order=
                index + 1,


            original=
                sentence,


            translation=
                translation_map.get(
                    index+1
                )

        )



        session.add(sentence_db)


        session.flush()



        tokens = analyze_sentence(
            sentence,
            source_language
        )



        for position,token in enumerate(tokens):


            word_db = ReadingWordDB(

                sentence_id=
                    sentence_db.id,


                word=
                    token["word"],


                lemma=
                    token["lemma"],


                pos=
                    token.get("pos"),


                position=
                    position+1

            )


            session.add(word_db)





    session.commit()







# =====================================================
# Background
# =====================================================


def process_reading(
    reading_id,
    payload
):


    session=SessionLocal()


    try:


        reading = (

            session.query(
                ReadingDB
            )
            .filter(
                ReadingDB.id==reading_id
            )
            .first()

        )


        if not reading:

            return




        # title

        if reading.title=="Generating title...":


            reading.title = generate_title(

                payload["content"],

                payload.get(
                    "source_language",
                    "de"
                )

            )


            session.commit()






        save_sentences(

            session,

            reading_id,

            payload["content"],

            payload.get(
                "source_language",
                "de"
            ),

            payload.get(
                "translation_language",
                "en"
            )

        )




        reading.status="completed"


        session.commit()



        print(
            "[READING COMPLETED]",
            reading_id
        )



    except Exception as e:


        print(
            "[READING ERROR]",
            e
        )


        session.rollback()



        reading = (

            session.query(
                ReadingDB
            )
            .filter(
                ReadingDB.id==reading_id
            )
            .first()

        )


        if reading:

            reading.status="failed"

            session.commit()



    finally:

        session.close()







# =====================================================
# POST /readings
# =====================================================


@router.post("/readings")
def create_reading_api(
    req:ReadingRequest,
    background_tasks:BackgroundTasks
):


    payload=req.model_dump()


    if not payload["content"].strip():

        raise HTTPException(
            400,
            "Content required"
        )



    reading_id=create_reading(
        payload
    )



    background_tasks.add_task(

        process_reading,

        reading_id,

        payload

    )



    return {

        "id":
            reading_id,


        "status":
            "processing"

    }








# =====================================================
# GET /readings
# =====================================================


@router.get("/readings")
def get_readings():


    session=SessionLocal()


    try:


        readings=(

            session.query(
                ReadingDB
            )
            .order_by(
                ReadingDB.id.desc()
            )
            .all()

        )



        return [

            {

                "id":
                    r.id,


                "title":
                    r.title,


                "difficulty":
                    r.difficulty,


                "status":
                    r.status,


                "source_language":
                    r.source_language,


                "translation_language":
                    r.translation_language

            }

            for r in readings

        ]


    finally:

        session.close()









# =====================================================
# GET /readings/{id}
# =====================================================


@router.get("/readings/{reading_id}")
def get_reading(reading_id:int):


    session=SessionLocal()


    try:


        reading=(

            session.query(
                ReadingDB
            )
            .filter(
                ReadingDB.id==reading_id
            )
            .first()

        )


        if not reading:

            raise HTTPException(
                404,
                "Reading not found"
            )



        sentences=[]



        db_sentences=(

            session.query(
                ReadingSentenceDB
            )
            .filter(
                ReadingSentenceDB.reading_id==reading_id
            )
            .order_by(
                ReadingSentenceDB.sentence_order
            )
            .all()

        )




        for s in db_sentences:


            words=[]



            db_words=(

                session.query(
                    ReadingWordDB
                )
                .filter(
                    ReadingWordDB.sentence_id==s.id
                )
                .order_by(
                    ReadingWordDB.position
                )
                .all()

            )



            for w in db_words:


                words.append({

                    "id":
                        w.id,

                    "word":
                        w.word,

                    "lemma":
                        w.lemma,

                    "pos":
                        w.pos,

                    "position":
                        w.position

                })




            sentences.append({

                "id":
                    s.id,


                "sentence_order":
                    s.sentence_order,


                "original":
                    s.original,


                "translation":
                    s.translation,


                "words":
                    words

            })




        return {

            "id":
                reading.id,


            "title":
                reading.title,


            "content":
                reading.content,


            "difficulty":
                reading.difficulty,


            "source_language":
                reading.source_language,


            "translation_language":
                reading.translation_language,


            "status":
                reading.status,


            "sentences":
                sentences

        }



    finally:

        session.close()