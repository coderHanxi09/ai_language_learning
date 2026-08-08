from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..db import SessionLocal

from ..models_db import (
    VocabularyDB,
    VocabularyTranslationDB,
    ReadingWordDB,
    ReadingSentenceDB,
    DictionaryEntryDB,
    DictionaryTranslationDB,
    FlashcardDB
)



router = APIRouter()





# =====================================================
# Request Model
# =====================================================


class VocabCreate(BaseModel):

    word: str

    lemma: str | None = None

    source_language: str = "de"

    workspace_id: int | None = None







# =====================================================
# Helper:
# get dictionary translation
# =====================================================


def _get_translation(
    dictionary_id: int,
    language: str = "en"
):


    session = SessionLocal()


    try:


        result = (

            session.query(
                DictionaryTranslationDB
            )

            .filter(
                DictionaryTranslationDB.dictionary_id
                ==
                dictionary_id
            )

            .filter(
                DictionaryTranslationDB.language
                ==
                language
            )

            .first()

        )


        if result:

            return result.translation


        return None


    finally:

        session.close()







# =====================================================
# Manual add vocabulary
# =====================================================


@router.post("")
def create_vocab(
    body: VocabCreate
):


    session = SessionLocal()


    try:


        word = body.word.strip()



        lemma = (

            body.lemma

            if body.lemma

            else word.lower()

        )



        # =========================
        # duplicate by lemma
        # =========================


        existing = (

            session.query(
                VocabularyDB
            )

            .filter(
                VocabularyDB.lemma
                ==
                lemma
            )

            .filter(
                VocabularyDB.source_language
                ==
                body.source_language
            )

            .first()

        )



        if existing:


            return {

                "message":
                    "already exists",

                "id":
                    existing.id

            }






        # =========================
        # dictionary lookup
        # =========================


        dictionary = (

            session.query(
                DictionaryEntryDB
            )

            .filter(
                DictionaryEntryDB.lemma
                ==
                lemma
            )

            .filter(
                DictionaryEntryDB.language
                ==
                body.source_language
            )

            .first()

        )



        vocab = VocabularyDB(

            word=word,

            lemma=lemma,

            source_language=
                body.source_language,

            dictionary_id=
                dictionary.id
                if dictionary
                else None,

            source="manual",

            workspace_id=
                body.workspace_id

        )



        session.add(
            vocab
        )


        session.flush()



        if dictionary:


            translation = _get_translation(

                dictionary.id,

                "en"

            )


            if translation:


                session.add(

                    VocabularyTranslationDB(

                        vocabulary_id=vocab.id,

                        language="en",

                        translation=translation

                    )

                )



                session.add(

                    FlashcardDB(

                        front=word,

                        back=translation,

                        vocabulary_id=vocab.id

                    )

                )



        session.commit()


        session.refresh(
            vocab
        )


        return {

            "message":
                "added",

            "id":
                vocab.id,

            "lemma":
                vocab.lemma

        }


    finally:

        session.close()







# =====================================================
# Add from reading
# =====================================================


@router.post("/from-reading")
def add_from_reading(
    body: dict
):


    word = body.get(
        "word"
    )


    reading_id = body.get(
        "reading_id"
    )



    if not word or not reading_id:


        raise HTTPException(

            400,

            "word and reading_id required"

        )



    session = SessionLocal()



    try:


        # =========================
        # find lemma from reading
        # =========================


        reading_word = (

            session.query(
                ReadingWordDB
            )

            .join(
                ReadingSentenceDB
            )

            .filter(
                ReadingSentenceDB.reading_id
                ==
                reading_id
            )

            .filter(
                ReadingWordDB.word
                ==
                word
            )

            .first()

        )



        lemma = (

            reading_word.lemma

            if reading_word

            else word.lower()

        )






        # =========================
        # duplicate
        # =========================


        existing = (

            session.query(
                VocabularyDB
            )

            .filter(
                VocabularyDB.lemma
                ==
                lemma
            )

            .filter(
                VocabularyDB.source_language
                ==
                "de"
            )

            .first()

        )



        if existing:


            return {

                "message":
                    "already exists",

                "id":
                    existing.id

            }







        # =========================
        # dictionary
        # =========================


        dictionary = (

            session.query(
                DictionaryEntryDB
            )

            .filter(
                DictionaryEntryDB.lemma
                ==
                lemma
            )

            .filter(
                DictionaryEntryDB.language
                ==
                "de"
            )

            .first()

        )



        vocab = VocabularyDB(

            word=word,

            lemma=lemma,

            source_language="de",

            dictionary_id=

                dictionary.id

                if dictionary

                else None,


            source="reading",

            reading_id=reading_id

        )



        session.add(
            vocab
        )


        session.flush()






        translation = None



        if dictionary:


            translation = _get_translation(

                dictionary.id,

                "en"

            )



        if translation:


            session.add(

                VocabularyTranslationDB(

                    vocabulary_id=vocab.id,

                    language="en",

                    translation=translation

                )

            )



            session.add(

                FlashcardDB(

                    front=word,

                    back=translation,

                    vocabulary_id=vocab.id

                )

            )





        session.commit()



        return {

            "message":
                "added",

            "id":
                vocab.id,

            "word":
                word,

            "lemma":
                lemma,

            "translation":
                translation

        }


    finally:

        session.close()







# =====================================================
# Get vocabulary list
# =====================================================


@router.get("")
def get_vocabularies():


    session = SessionLocal()


    try:


        items = (

            session.query(
                VocabularyDB
            )

            .order_by(
                VocabularyDB.id.desc()
            )

            .all()

        )



        result = []



        for item in items:


            translations = [

                {

                    "language":t.language,

                    "translation":t.translation

                }

                for t in item.translations

            ]



            result.append(

                {

                    "id":
                        item.id,

                    "word":
                        item.word,

                    "lemma":
                        item.lemma,

                    "source_language":
                        item.source_language,

                    "translations":
                        translations

                }

            )



        return result



    finally:

        session.close()







# =====================================================
# Get one vocabulary
# =====================================================


@router.get("/{word}")
def get_vocab(
    word:str
):


    session = SessionLocal()


    try:


        vocab = (

            session.query(
                VocabularyDB
            )

            .filter(
                VocabularyDB.lemma
                ==
                word.lower()
            )

            .first()

        )


        if not vocab:


            raise HTTPException(

                404,

                "vocabulary not found"

            )



        return {


            "id":
                vocab.id,


            "word":
                vocab.word,


            "lemma":
                vocab.lemma,


            "translations":

                [

                    {

                    "language":t.language,

                    "translation":t.translation

                    }

                    for t in vocab.translations

                ]

        }



    finally:

        session.close()







# =====================================================
# Delete vocabulary
# =====================================================


@router.delete("/{word}")
def delete_vocab(
    word:str
):


    session = SessionLocal()


    try:


        vocab = (

            session.query(
                VocabularyDB
            )

            .filter(
                VocabularyDB.lemma
                ==
                word.lower()
            )

            .first()

        )


        if not vocab:


            raise HTTPException(

                404,

                "vocabulary not found"

            )



        session.delete(
            vocab
        )


        session.commit()



        return {

            "message":
                "deleted",

            "lemma":
                word.lower()

        }


    finally:

        session.close()