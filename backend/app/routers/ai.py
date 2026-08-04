from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

from ..services.ai_service import generate_reading
from ..services.sentence_service import split_sentences

from ..db import SessionLocal
from ..models_db import (
    ReadingDB,
    ReadingSentenceDB
)

import json


router = APIRouter()



class ReadingRequest(BaseModel):

    topic: str

    difficulty: str = "B2"

    known_vocabulary: list[str] = []




def _create_initial_reading(
    payload: dict
):

    """
    Create empty reading before AI generation.
    """


    session = SessionLocal()


    try:


        print(
            "[DB] Creating initial reading"
        )


        rd = ReadingDB(

            title="Generating...",

            topic=payload.get(
                "topic"
            ),

            difficulty=payload.get(
                "difficulty",
                "B2"
            ),

            content="",

            vocabulary=json.dumps([]),

            status="generating"

        )


        session.add(rd)

        session.commit()

        session.refresh(rd)


        print(
            f"[DB] Created reading id={rd.id}"
        )


        return rd.id



    finally:

        session.close()





def _save_sentences(
    session,
    reading_id: int,
    content: str
):

    """
    Split article and save sentences.
    """


    print(
        "[DB] Creating sentences"
    )


    sentences = split_sentences(
        content
    )


    for index, sentence in enumerate(sentences):


        obj = ReadingSentenceDB(

            reading_id=reading_id,

            sentence_order=index + 1,

            original=sentence,

            translation=None

        )


        session.add(obj)



    print(
        f"[DB] Saved {len(sentences)} sentences"
    )





def _update_reading_success(
    reading_id: int,
    data: dict
):

    """
    Update completed reading.
    """


    session = SessionLocal()


    try:


        print(
            "[DB] Updating completed reading"
        )


        reading = session.query(
            ReadingDB
        ).filter(
            ReadingDB.id == reading_id
        ).first()



        if not reading:

            return



        reading.title = data.get(
            "title"
        )


        reading.content = data.get(
            "content"
        )


        reading.vocabulary = json.dumps(
            data.get(
                "vocabulary",
                []
            )
        )


        reading.status = "completed"



        # create sentences

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
            "[DB] Reading completed"
        )



    except Exception as e:


        print(
            "[DB ERROR]",
            e
        )


        session.rollback()

        raise



    finally:

        session.close()





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

        "status": "generating",

        "message":
            "Reading generation started"

    }






def _background_generate_and_update(
    reading_id:int,
    payload:dict
):


    print(
        "[TASK] Started"
    )


    try:


        reading = generate_reading(

            payload.get(
                "topic"
            ),

            payload.get(
                "difficulty"
            ),

            payload.get(
                "known_vocabulary",
                []
            )

        )


        print(
            "[AI] Generation finished"
        )


        _update_reading_success(

            reading_id,

            reading

        )



    except Exception as e:


        print(
            "[AI ERROR]",
            e
        )


        _update_reading_failed(
            reading_id
        )






@router.get("/readings")
def get_readings():


    session = SessionLocal()


    try:


        readings = session.query(
            ReadingDB
        ).order_by(
            ReadingDB.id.desc()
        ).all()



        result=[]


        for reading in readings:


            result.append({

                "id":reading.id,

                "title":reading.title,

                "topic":reading.topic,

                "difficulty":reading.difficulty,

                "status":reading.status,

                "content":reading.content,

                "vocabulary":json.loads(
                    reading.vocabulary or "[]"
                ),

                "created_at":reading.created_at

            })


        return result



    finally:

        session.close()






@router.get("/readings/{reading_id}")
def get_reading(
    reading_id:int
):


    session=SessionLocal()


    try:


        reading=session.query(
            ReadingDB
        ).filter(
            ReadingDB.id==reading_id
        ).first()



        if not reading:


            raise HTTPException(

                status_code=404,

                detail="Reading not found"

            )



        return {

            "id":reading.id,

            "title":reading.title,

            "topic":reading.topic,

            "difficulty":reading.difficulty,

            "status":reading.status,

            "content":reading.content,

            "vocabulary":json.loads(
                reading.vocabulary or "[]"
            )

        }



    finally:

        session.close()