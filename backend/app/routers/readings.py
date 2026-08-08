from fastapi import (
    APIRouter,
    BackgroundTasks,
    HTTPException
)

from pydantic import BaseModel, Field

import json


from ..services.ai_service import (
    generate_reading
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


from ..services.dictionary_service import (
    lookup_words
)


from ..db import SessionLocal


from ..models_db import (
    ReadingDB,
    ReadingSentenceDB,
    ReadingWordDB
)



router = APIRouter()





# =====================================================
# Request Model
# =====================================================


class ReadingRequest(BaseModel):

    topic: str


    difficulty: str = "B2"


    # language of generated article
    # de / en
    source_language: str = "de"


    # translation language
    # en / zh
    translation_language: str = "en"



    known_vocabulary: list[str] = Field(
        default_factory=list
    )







# =====================================================
# Create initial reading
# =====================================================


def _create_initial_reading(
    payload: dict
):

    session = SessionLocal()


    try:


        reading = ReadingDB(

            title="Generating...",


            topic=payload["topic"],


            difficulty=payload.get(
                "difficulty",
                "B2"
            ),


            source_language=payload.get(
                "source_language",
                "de"
            ),


            translation_language=payload.get(
                "translation_language",
                "en"
            ),


            content="",


            vocabulary=json.dumps(
                []
            ),


            status="generating"

        )


        session.add(
            reading
        )


        session.commit()


        session.refresh(
            reading
        )


        return reading.id



    finally:

        session.close()







# =====================================================
# Save sentences and words
# =====================================================


def _save_sentences(
    session,
    reading_id: int,
    content: str,
    source_language: str,
    translation_language: str
):


    sentences = split_sentences(
        content
    )



    translations = translate_sentences(

        sentences,

        source_language,

        translation_language

    )



    translation_map = {

        item["sentence_order"]:
            item["translation"]

        for item in translations

    }




    for index, sentence in enumerate(sentences):


        order = index + 1



        sentence_obj = ReadingSentenceDB(

            reading_id=reading_id,


            sentence_order=order,


            original=sentence,


            translation=translation_map.get(
                order
            )

        )


        session.add(
            sentence_obj
        )


        session.flush()





        # =========================
        # NLP analysis
        # =========================


        tokens = analyze_sentence(
            sentence
        )




        for position, token in enumerate(tokens):


            word_obj = ReadingWordDB(

                sentence_id=sentence_obj.id,


                word=token["word"],


                lemma=token["lemma"],


                position=position + 1

            )


            session.add(
                word_obj
            )







# =====================================================
# Update success
# =====================================================


def _update_reading_success(
    reading_id:int,
    data:dict,
    source_language:str,
    translation_language:str
):


    session = SessionLocal()


    try:


        reading = session.query(
            ReadingDB
        ).filter(
            ReadingDB.id == reading_id
        ).first()



        if not reading:

            return





        reading.title = data.get(
            "title",
            "Reading"
        )


        reading.content = data.get(
            "content",
            ""
        )


        reading.vocabulary = json.dumps(

            data.get(
                "vocabulary",
                []
            ),

            ensure_ascii=False

        )



        reading.status = "completed"




        _save_sentences(

            session,


            reading_id,


            data.get(
                "content",
                ""
            ),


            source_language,


            translation_language

        )



        session.commit()



        print(
            "[READING] completed"
        )



    except Exception as e:


        session.rollback()

        raise e



    finally:

        session.close()







# =====================================================
# Update failed
# =====================================================


def _update_reading_failed(
    reading_id:int
):


    session = SessionLocal()


    try:


        reading = session.query(
            ReadingDB
        ).filter(
            ReadingDB.id == reading_id
        ).first()



        if reading:

            reading.status="failed"

            session.commit()



    finally:

        session.close()







# =====================================================
# Background generation
# =====================================================


def _background_generate_and_update(
    reading_id,
    payload
):


    try:


        print(
            "[READING] generating",
            payload
        )



        result = generate_reading(

            payload["topic"],


            payload.get(
                "difficulty",
                "B2"
            ),


            payload.get(
                "source_language",
                "de"
            ),


            payload.get(
                "translation_language",
                "en"
            ),


            payload.get(
                "known_vocabulary",
                []
            )

        )





        _update_reading_success(

            reading_id,


            result,


            payload.get(
                "source_language",
                "de"
            ),


            payload.get(
                "translation_language",
                "en"
            )

        )





    except Exception as e:


        print(
            "[READING ERROR]",
            e
        )


        _update_reading_failed(
            reading_id
        )









# =====================================================
# POST /readings
# =====================================================


@router.post("/readings")
def create_reading(
    req: ReadingRequest,
    background_tasks: BackgroundTasks
):


    payload = req.model_dump()



    reading_id = _create_initial_reading(
        payload
    )



    background_tasks.add_task(

        _background_generate_and_update,


        reading_id,


        payload

    )



    return {

        "id": reading_id,


        "status": "generating"

    }









# =====================================================
# GET /readings
# =====================================================


@router.get("/readings")
def get_readings():


    session = SessionLocal()



    try:


        readings = session.query(
            ReadingDB
        ).order_by(
            ReadingDB.id.desc()
        ).all()




        return [

            {

                "id": r.id,


                "title": r.title,


                "status": r.status,


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
def get_reading(
    reading_id:int
):


    session = SessionLocal()



    try:


        reading = session.query(
            ReadingDB
        ).filter(
            ReadingDB.id == reading_id
        ).first()




        if not reading:


            raise HTTPException(

                status_code=404,

                detail="Reading not found"

            )





        sentences=[]




        for sentence in reading.sentences:


            words=[]



            for word in sentence.words:


                words.append(

                    {

                        "id":word.id,


                        "word":word.word,


                        "lemma":word.lemma,


                        "position":word.position

                    }

                )



            sentences.append(

                {

                    "id":sentence.id,


                    "sentence_order":
                        sentence.sentence_order,


                    "original":
                        sentence.original,


                    "translation":
                        sentence.translation,


                    "words":words

                }

            )





        return {


            "id":reading.id,


            "title":reading.title,


            "topic":reading.topic,


            "difficulty":reading.difficulty,


            "source_language":
                reading.source_language,


            "translation_language":
                reading.translation_language,


            "status":reading.status,


            "content":reading.content,


            "sentences":sentences

        }



    finally:

        session.close()