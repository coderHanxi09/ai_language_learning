from fastapi import (
    APIRouter,
    HTTPException,
    BackgroundTasks
)

from pydantic import BaseModel

import random


from ..db import SessionLocal


from ..models_db import (
    VocabularyDB,
    ReadingDB
)


from ..ai.factory import get_ai_provider


from .readings import process_reading



router = APIRouter()





# =====================================================
# Request
# =====================================================


class WritingRequest(BaseModel):

    language: str = "de"

    level: str = "B2"







# =====================================================
# Generate Article with AI
# =====================================================


def generate_article(

    words,

    language,

    level

):


    provider = get_ai_provider()



    vocabulary_text = ", ".join(

        [

            word.lemma

            for word in words

        ]

    )





    language_name = (

        "German"

        if language == "de"

        else

        "English"

    )






    prompt = f"""

Write a {language_name} language learning article.

Requirements:

- Language: {language_name}
- Level: {level}
- Length: around 400 words
- Use all vocabulary words naturally.
- The article must be coherent.
- Do not create a vocabulary list.
- Do not explain the vocabulary words.
- Return ONLY the article text.


Vocabulary words:

{vocabulary_text}

"""





    result = provider.generate(

        prompt

    )



    return result.strip()







# =====================================================
# Save Reading
# =====================================================


def save_reading(

    content,

    language,

    level

):

    session = SessionLocal()


    try:


        translation_language = (

            "en"

            if language == "de"

            else

            "de"

        )


        reading = ReadingDB(

            title="Generating title...",

            content=content,

            source_language=language,

            translation_language=translation_language,

            difficulty=level,

            vocabulary="[]",

            status="processing"

        )


        session.add(reading)

        session.commit()

        session.refresh(reading)


        return reading.id


    finally:

        session.close()




# =====================================================
# POST /writing/generate
# =====================================================


@router.post("/generate")
def generate_writing(

    req: WritingRequest,

    background_tasks: BackgroundTasks

):


    session = SessionLocal()



    try:



        vocabulary = (

            session.query(

                VocabularyDB

            )

            .filter(

                VocabularyDB.source_language

                ==

                req.language

            )

            .order_by(

                VocabularyDB.id.asc()

            )

            .all()

        )





        if not vocabulary:



            raise HTTPException(

                status_code=400,

                detail="No vocabulary found for this language"

            )






        selected_words = random.sample(

            vocabulary,

            min(

                50,

                len(vocabulary)

            )

        )



    finally:


        session.close()







    # =========================
    # AI Generation
    # =========================


    try:



        article = generate_article(

            selected_words,

            req.language,

            req.level

        )



    except Exception as e:



        raise HTTPException(

            status_code=500,

            detail=f"AI generation failed: {str(e)}"

        )







    # =========================
    # Create Reading
    # =========================


    reading_id = save_reading(

        article,

        req.language,

        req.level

    )








    translation_language = (

        "en"

        if req.language == "de"

        else

        "de"

    )








    background_tasks.add_task(

        process_reading,

        reading_id,

        {


            "content": article,


            "source_language": req.language,


            "translation_language": translation_language,


            "difficulty": req.level


        }

    )







    return {


        "id":

            reading_id,


        "status":

            "processing"

    }