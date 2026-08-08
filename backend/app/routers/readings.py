from fastapi import (
    APIRouter,
    BackgroundTasks,
    HTTPException
)

from pydantic import BaseModel, Field

import json


from ..services.translation_service import (
    translate_sentences
)


from ..services.sentence_service import (
    split_sentences
)


from ..services.word_token_service import (
    analyze_sentence
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

class ReadingCreateRequest(BaseModel):

    title: str


    content: str


    # de / en
    source_language: str = "de"


    # en / zh
    translation_language: str = "en"


    difficulty: str = "B2"


    known_vocabulary: list[str] = Field(
        default_factory=list
    )







# =====================================================
# Create Reading
# =====================================================

def _create_reading(
    payload: dict
):

    session = SessionLocal()

    try:

        reading = ReadingDB(

            title=payload["title"],

            topic=None,

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

            content=payload["content"],

            vocabulary=json.dumps(
                [],
                ensure_ascii=False
            ),

            status="processing"

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
# Save sentences + words
# =====================================================

def _process_sentences(
    reading_id: int,
    content: str,
    source_language: str,
    translation_language: str
):

    session = SessionLocal()


    try:


        sentences = split_sentences(
            content
        )


        translations = translate_sentences(
            sentences
        )


        translation_map = {

            item["sentence_order"]:
                item["translation"]

            for item in translations

        }



        for index, sentence in enumerate(sentences):


            sentence_order = index + 1



            sentence_db = ReadingSentenceDB(

                reading_id=reading_id,

                sentence_order=sentence_order,

                original=sentence,

                translation=translation_map.get(
                    sentence_order
                )

            )


            session.add(
                sentence_db
            )


            session.flush()



            # =========================
            # German NLP
            # =========================

            words = analyze_sentence(
                sentence,
                language=source_language
            )



            for position, word in enumerate(words):


                word_db = ReadingWordDB(

                    sentence_id=sentence_db.id,

                    word=word["word"],

                    lemma=word["lemma"],

                    pos=word["pos"],

                    position=position + 1

                )


                session.add(
                    word_db
                )



        reading = session.query(
            ReadingDB
        ).filter(
            ReadingDB.id == reading_id
        ).first()



        reading.status = "completed"



        session.commit()



    except Exception as e:


        session.rollback()


        reading = session.query(
            ReadingDB
        ).filter(
            ReadingDB.id == reading_id
        ).first()


        if reading:

            reading.status="failed"

            session.commit()


        raise e



    finally:

        session.close()








# =====================================================
# Background task
# =====================================================

def _background_process_reading(
    reading_id:int,
    content:str,
    source_language:str,
    translation_language:str
):


    try:

        print(
            "[READING] processing",
            reading_id
        )


        _process_sentences(

            reading_id,

            content,

            source_language,

            translation_language

        )


        print(
            "[READING] completed"
        )


    except Exception as e:

        print(
            "[READING ERROR]",
            e
        )








# =====================================================
# POST /readings
# =====================================================

@router.post("/readings")
def create_reading(

    req: ReadingCreateRequest,

    background_tasks: BackgroundTasks

):


    payload = req.model_dump()



    reading_id = _create_reading(
        payload
    )



    background_tasks.add_task(

        _background_process_reading,

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



    return {

        "id": reading_id,

        "status": "processing"

    }








# =====================================================
# GET all readings
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
                    r.translation_language,

                "difficulty":
                    r.difficulty

            }

            for r in readings

        ]


    finally:

        session.close()







# =====================================================
# GET reading detail
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

                        "id": word.id,

                        "word": word.word,

                        "lemma": word.lemma,

                        "pos": word.pos,

                        "position": word.position

                    }

                )



            sentences.append(

                {

                    "id": sentence.id,

                    "sentence_order":
                        sentence.sentence_order,

                    "original":
                        sentence.original,

                    "translation":
                        sentence.translation,

                    "words":
                        words

                }

            )



        return {

            "id": reading.id,

            "title": reading.title,

            "difficulty": reading.difficulty,

            "source_language":
                reading.source_language,

            "translation_language":
                reading.translation_language,

            "status": reading.status,

            "content": reading.content,

            "sentences": sentences

        }


    finally:

        session.close()