from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field

import json
import traceback


from ..services.ai_service import generate_reading

from ..services.sentence_service import (
    split_sentences
)

from ..services.translation_service import (
    translate_sentences
)

from ..services.vocabulary_sync_service import (
    sync_vocabulary_to_dictionary
)

from ..services.dictionary_service import (
    lookup_words
)

from ..services.word_token_service import (
    tokenize_sentence,
    normalize_word
)

from ..db import SessionLocal

from ..models_db import (
    ReadingDB,
    ReadingSentenceDB,
    ReadingWordDB
)


router = APIRouter()


# =========================
# Request Model
# =========================

class ReadingRequest(BaseModel):

    topic: str

    difficulty: str = "B2"

    known_vocabulary: list[str] = Field(
        default_factory=list
    )


# =========================
# Create initial reading
# =========================

def _create_initial_reading(
    payload: dict
):

    session = SessionLocal()

    try:

        reading = ReadingDB(

            title="Generating...",

            topic=payload.get(
                "topic"
            ),

            difficulty=payload.get(
                "difficulty",
                "B2"
            ),

            content="",

            vocabulary=json.dumps(
                []
            ),

            status="generating"

        )


        session.add(reading)

        session.commit()

        session.refresh(reading)


        return reading.id


    finally:

        session.close()



# =========================
# Save sentences and words
# =========================

def _save_sentences(
    session,
    reading_id: int,
    content: str
):

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



        tokens = tokenize_sentence(
            sentence
        )


        for position, token in enumerate(tokens):

            word_obj = ReadingWordDB(

                sentence_id=sentence_obj.id,

                word=token,

                lemma=normalize_word(
                    token
                ),

                position=position + 1

            )


            session.add(
                word_obj
            )


    print(
        "[DB] Sentences and words saved"
    )



# =========================
# Update success
# =========================

def _update_reading_success(
    reading_id: int,
    data: dict
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
            "Untitled"
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



        sync_vocabulary_to_dictionary(

            data.get(
                "vocabulary",
                []
            )

        )



        _save_sentences(

            session,

            reading_id,

            data.get(
                "content",
                ""
            )

        )


        session.commit()


        print(
            "[READING] completed"
        )


    finally:

        session.close()



# =========================
# Update failed
# =========================

def _update_reading_failed(
    reading_id: int
):

    session = SessionLocal()

    try:

        reading = session.query(
            ReadingDB
        ).filter(
            ReadingDB.id == reading_id
        ).first()


        if reading:

            reading.status = "failed"

            session.commit()


    finally:

        session.close()



# =========================
# Background generation
# =========================

def _background_generate_and_update(
    reading_id,
    payload
):

    try:

        print(
            "[READING] generating:",
            payload
        )


        result = generate_reading(

            payload["topic"],

            payload["difficulty"],

            payload.get(
                "known_vocabulary",
                []
            )

        )


        print(
            "[READING] AI result:",
            result
        )


        _update_reading_success(

            reading_id,

            result

        )


    except Exception as e:


        print(
            "[READING ERROR]",
            e
        )


        traceback.print_exc()


        _update_reading_failed(
            reading_id
        )



# =========================
# POST /readings
# =========================

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



# =========================
# GET /readings
# =========================

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

                "status": r.status

            }

            for r in readings

        ]


    finally:

        session.close()



# =========================
# GET /readings/{id}
# =========================

@router.get("/readings/{reading_id}")
def get_reading(
    reading_id: int
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


        sentences = []


        for sentence in reading.sentences:


            words = [

                w.word

                for w in sentence.words

            ]


            dictionary = lookup_words(
                words
            )


            sentences.append({

                "sentence_order":
                    sentence.sentence_order,

                "original":
                    sentence.original,

                "translation":
                    sentence.translation,

                "words": [

                    {

                        "word": w,

                        "dictionary":
                            dictionary.get(
                                w.lower()
                            )

                    }

                    for w in words

                ]

            })


        return {

            "id": reading.id,

            "title": reading.title,

            "topic": reading.topic,

            "difficulty": reading.difficulty,

            "status": reading.status,

            "content": reading.content,

            "sentences": sentences

        }


    finally:

        session.close()