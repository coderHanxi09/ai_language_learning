from contextlib import asynccontextmanager
import json

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .routers import (
    dictionary,
    ai,
    workspace,
    vocabulary,
    flashcards,
    auth,
    readings,
    writing,
)


from .db import (
    init_db,
    SessionLocal
)


from .models_db import (
    DictionaryEntryDB,
    DictionaryTranslationDB
)





# =====================================================
# Load environment variables
# =====================================================

load_dotenv()







# =====================================================
# Database seed
# =====================================================


def seed_dictionary():


    session = SessionLocal()


    try:


        count = (

            session.query(
                DictionaryEntryDB
            )

            .count()

        )



        if count > 0:

            return






        # =====================================================
        # Seed dictionary entries
        # =====================================================


        samples = [

            {


                "word": "apple",

                "lemma": "apple",

                "language": "en",

                "pos": "noun",

                "cefr": "A1",

                "ipa": "/ˈæpəl/",

                "examples": json.dumps(

                    [

                        "She ate an apple for breakfast."

                    ],

                    ensure_ascii=False

                )

            },



            {


                "word": "serendipity",

                "lemma": "serendipity",

                "language": "en",

                "pos": "noun",

                "cefr": "C1",

                "ipa": "/ˌserənˈdɪpəti/",

                "examples": json.dumps(

                    [

                        "Finding the manuscript was pure serendipity."

                    ],

                    ensure_ascii=False

                )

            },



            # German example

            {


                "word": "Entscheidung",

                "lemma": "Entscheidung",

                "language": "de",

                "pos": "noun",

                "cefr": "B1",

                "ipa": "/ɛntˈʃaɪ̯dʊŋ/",

                "examples": json.dumps(

                    [

                        "Das war eine schwierige Entscheidung."

                    ],

                    ensure_ascii=False

                )

            },


        ]





        created_entries = {}





        for sample in samples:


            entry = DictionaryEntryDB(

                **sample

            )


            session.add(entry)


            session.flush()



            created_entries[

                (
                    sample["lemma"],

                    sample["language"]

                )

            ] = entry.id







        # =====================================================
        # Seed translations
        # =====================================================


        translations = [



            {


                "dictionary_id":

                    created_entries[

                        (
                            "apple",

                            "en"

                        )

                    ],

                "language":

                    "de",

                "translation":

                    "Apfel"


            },



            {


                "dictionary_id":

                    created_entries[

                        (
                            "serendipity",

                            "en"

                        )

                    ],

                "language":

                    "de",

                "translation":

                    "glücklicher Zufall"


            },



            {


                "dictionary_id":

                    created_entries[

                        (
                            "Entscheidung",

                            "de"

                        )

                    ],

                "language":

                    "en",

                "translation":

                    "decision"


            },


        ]





        for item in translations:


            session.add(

                DictionaryTranslationDB(

                    **item

                )

            )






        session.commit()



        print(
            "[DB] Dictionary seeded"
        )



    except Exception as e:


        session.rollback()


        print(

            "[DB SEED ERROR]",

            e

        )


        raise



    finally:


        session.close()







# =====================================================
# Lifespan
# =====================================================


@asynccontextmanager
async def lifespan(
    app: FastAPI
):


    print(
        "[APP] Initializing database..."
    )


    init_db()



    print(
        "[APP] Seeding dictionary..."
    )


    seed_dictionary()



    print(
        "[APP] Startup complete."
    )



    yield



    print(
        "[APP] Shutdown."
    )









# =====================================================
# FastAPI
# =====================================================


app = FastAPI(

    title="AI Reading Workspace Backend",

    lifespan=lifespan

)








# =====================================================
# CORS
# =====================================================


app.add_middleware(

    CORSMiddleware,


    allow_origins=[


        "http://localhost:5173",

        "http://127.0.0.1:5173",


        "http://localhost:3000",

        "http://127.0.0.1:3000",

    ],


    allow_credentials=True,


    allow_methods=["*"],


    allow_headers=["*"],

)








# =====================================================
# Routers
# =====================================================



app.include_router(

    dictionary.router,

    prefix="/dictionary",

    tags=["Dictionary"]

)



app.include_router(

    ai.router,

    prefix="/ai",

    tags=["AI"]

)



app.include_router(

    readings.router,

    tags=["Readings"]

)



app.include_router(

    workspace.router,

    prefix="/workspace",

    tags=["Workspace"]

)



app.include_router(

    vocabulary.router,

    prefix="/vocabulary",

    tags=["Vocabulary"]

)



app.include_router(

    flashcards.router,

    prefix="/flashcards",

    tags=["Flashcards"]

)

app.include_router(

    writing.router,

    prefix="/writing",

    tags=["Writing"]

)

app.include_router(

    auth.router,

    prefix="/auth",

    tags=["Authentication"]

)








# =====================================================
# Root
# =====================================================


@app.get("/")
def root():


    return {


        "status":

            "ok",


        "service":

            "AI Reading Workspace Backend"

    }