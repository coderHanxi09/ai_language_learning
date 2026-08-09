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
# Generate title
# =====================================================


def generate_title(

    content: str,

    source_language: str = "de"

):


    if not content:

        return "Imported Reading"



    provider = get_ai_provider()



    language_name = (

        "German"

        if source_language == "de"

        else

        "English"

    )



    prompt = f"""
Generate a short and meaningful title for this
{language_name} reading article.

Requirements:

- Language: {language_name}
- Maximum 8 words
- Do not use quotation marks
- Do not summarize too much
- Return ONLY the title

Article:

{content[:2000]}
"""



    try:


        title = provider.generate(

            prompt

        ).strip()



        if title:

            return title



    except Exception as e:


        print(

            "[TITLE GENERATION ERROR]",

            e

        )





    # =========================
    # Fallback
    # =========================

    sentences = split_sentences(

        content

    )



    if sentences:


        words = sentences[0].split()



        if len(words) > 8:


            return (

                " ".join(

                    words[:8]

                )

                +

                "..."

            )



        return sentences[0]



    return "Imported Reading"









# =====================================================
# Create Reading
# =====================================================


def create_reading(

    payload: dict

):


    session = SessionLocal()



    try:


        title = payload.get(

            "title"

        )



        # If no title was supplied,
        # leave a temporary title.
        # process_reading() will generate
        # the correct language title later.

        if not title:


            title = "Generating title..."





        reading = ReadingDB(


            title=title,


            content=payload["content"],


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
# Save sentences
# =====================================================


def save_sentences(

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





    translation_map = {}





    for item in translations:


        translation_map[

            item["sentence_order"]

        ] = item["translation"]









    for index, sentence in enumerate(

        sentences

    ):


        sentence_db = ReadingSentenceDB(


            reading_id=reading_id,


            sentence_order=index + 1,


            original=sentence,


            translation=translation_map.get(

                index + 1

            )

        )



        session.add(

            sentence_db

        )


        session.flush()





        tokens = analyze_sentence(

            sentence,

            source_language

        )





        for position, token in enumerate(

            tokens

        ):


            word_db = ReadingWordDB(


                sentence_id=sentence_db.id,


                word=token["word"],


                lemma=token["lemma"],


                pos=token.get(

                    "pos"

                ),


                position=position + 1

            )


            session.add(

                word_db

            )









# =====================================================
# Background Processing
# =====================================================


def process_reading(

    reading_id: int,

    payload: dict

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





        # =========================
        # Generate title only when
        # no meaningful title exists
        # =========================

        current_title = reading.title



        if (

            not current_title

            or

            current_title == "Generating title..."

        ):


            try:


                reading.title = generate_title(

                    payload["content"],

                    payload.get(

                        "source_language",

                        "de"

                    )

                )



                session.commit()



            except Exception as e:


                print(

                    "[TITLE ERROR]",

                    e

                )


                reading.title = "Imported Reading"


                session.commit()







        # =========================
        # Save sentences
        # =========================

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





        # =========================
        # Completed
        # =========================

        reading.status = "completed"



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









# =====================================================
# POST /readings
# =====================================================


@router.post("/readings")
def create_reading_api(

    req: ReadingRequest,

    background_tasks: BackgroundTasks

):


    payload = req.model_dump()



    if not payload.get(

        "content"

    ):


        raise HTTPException(

            status_code=400,

            detail="Content is required"

        )





    reading_id = create_reading(

        payload

    )





    # Run translation,
    # tokenization and title generation
    # in background.

    background_tasks.add_task(

        process_reading,

        reading_id,

        payload

    )





    return {


        "id":

            reading_id,


        "title":

            payload.get(

                "title"

            )

            or

            "Generating title...",


        "status":

            "processing"

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


                "id":

                    reading.id,


                "title":

                    reading.title,


                "difficulty":

                    reading.difficulty,


                "status":

                    reading.status,


                "source_language":

                    reading.source_language,


                "translation_language":

                    reading.translation_language


            }


            for reading in readings


        ]



    finally:


        session.close()









# =====================================================
# GET /readings/{reading_id}
# =====================================================


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


            words = []



            for word in sentence.words:


                words.append(

                    {


                        "id":

                            word.id,


                        "word":

                            word.word,


                        "lemma":

                            word.lemma,


                        "pos":

                            word.pos,


                        "position":

                            word.position

                    }

                )





            sentences.append(

                {


                    "id":

                        sentence.id,


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