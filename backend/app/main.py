from contextlib import asynccontextmanager
import json

from dotenv import load_dotenv
from fastapi import FastAPI

from .routers import (
    dictionary,
    ai,
    workspace,
    vocabulary,
    flashcards,
    auth,
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
        count = session.query(DictionaryEntryDB).count()

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

                entry = DictionaryEntryDB(
                    **sample
                )

                session.add(entry)


            session.commit()


    finally:

        session.close()



# =========================
# Application lifespan
# =========================

@asynccontextmanager
async def lifespan(app: FastAPI):

    # startup

    init_db()

    seed_dictionary()


    yield


    # shutdown
    # future cleanup can be added here



# =========================
# FastAPI app
# =========================

app = FastAPI(
    title="AI Reading Workspace - Backend",
    lifespan=lifespan,
)



# =========================
# Routers
# =========================

app.include_router(
    dictionary.router,
    prefix="/dictionary",
    tags=["dictionary"],
)

app.include_router(
    ai.router,
    prefix="/ai",
    tags=["ai"],
)

app.include_router(
    workspace.router,
    prefix="/workspace",
    tags=["workspace"],
)

app.include_router(
    vocabulary.router,
    prefix="/vocabulary",
    tags=["vocabulary"],
)

app.include_router(
    flashcards.router,
    prefix="/flashcards",
    tags=["flashcards"],
)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)



# =========================
# Health check
# =========================

@app.get("/")
def read_root():

    return {
        "status": "ok",
        "service": "AI Reading Workspace Backend",
    }