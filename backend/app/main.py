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
)


from .db import init_db, SessionLocal
from .models_db import DictionaryEntryDB



# =========================
# Load environment variables
# =========================

load_dotenv()



# =========================
# Database seed
# =========================

def seed_dictionary():

    session = SessionLocal()

    try:

        count = session.query(
            DictionaryEntryDB
        ).count()


        if count == 0:


            samples = [

                {
                    "word": "serendipity",
                    "lemma": "serendipity",
                    "definition": (
                        "the occurrence of events by chance "
                        "in a happy or beneficial way"
                    ),
                    "pos": "noun",
                    "cefr": "C1",
                    "ipa": "/ˌsɛrənˈdɪpɪti/",
                    "examples": json.dumps(
                        [
                            "Finding the manuscript was pure serendipity."
                        ]
                    ),
                },


                {
                    "word": "apple",
                    "lemma": "apple",
                    "definition": (
                        "a round fruit with red or green skin"
                    ),
                    "pos": "noun",
                    "cefr": "A1",
                    "ipa": "/ˈæpəl/",
                    "examples": json.dumps(
                        [
                            "She ate an apple for breakfast."
                        ]
                    ),
                },

            ]


            for sample in samples:

                session.add(
                    DictionaryEntryDB(**sample)
                )


            session.commit()


    finally:

        session.close()



# =========================
# Lifespan
# =========================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("[APP] Initializing database...")

    init_db()


    print("[APP] Seeding dictionary...")

    seed_dictionary()


    print("[APP] Startup complete.")


    yield


    print("[APP] Shutdown.")



# =========================
# FastAPI
# =========================

app = FastAPI(

    title="AI Reading Workspace Backend",

    lifespan=lifespan

)



# =========================
# CORS
# =========================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:5174",

        "http://127.0.0.1:5173",

        "http://localhost:3000",

        "http://127.0.0.1:3000",

    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)



# =========================
# Routers
# =========================


app.include_router(

    dictionary.router,

    prefix="/dictionary",

    tags=["Dictionary"],

)



app.include_router(

    ai.router,

    prefix="/ai",

    tags=["AI"],

)



app.include_router(

    readings.router,

    tags=["Readings"],

)



app.include_router(

    workspace.router,

    prefix="/workspace",

    tags=["Workspace"],

)



app.include_router(

    vocabulary.router,

    prefix="/vocabulary",

    tags=["Vocabulary"],

)



app.include_router(

    flashcards.router,

    prefix="/flashcards",

    tags=["Flashcards"],

)



app.include_router(

    auth.router,

    prefix="/auth",

    tags=["Authentication"],

)




# =========================
# Root
# =========================

@app.get("/")
def root():

    return {

        "status": "ok",

        "service": "AI Reading Workspace Backend"

    }