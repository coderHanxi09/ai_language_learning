from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

from ..db import SessionLocal

from ..models_db import (
    VocabularyDB,
    VocabularyTranslationDB
)

from ..services.dictionary_service import (
    lookup_word
)


router = APIRouter()





# =====================================================
# Request
# =====================================================

class VocabularyRequest(BaseModel):

    word: str

    language: str = "de"









# =====================================================
# Add vocabulary
# =====================================================

@router.post("")
def add_vocabulary(
    req: VocabularyRequest
):


    word = req.word.strip()


    if not word:

        raise HTTPException(

            status_code=400,

            detail="Word required"

        )



    # =================================================
    # Always get dictionary information
    # =================================================


    dictionary = lookup_word(

        word,

        req.language

    )



    if not dictionary:


        raise HTTPException(

            status_code=404,

            detail="Dictionary entry not found"

        )







    session = SessionLocal()



    try:


        lemma = dictionary.get(

            "lemma",

            word

        )




        # check duplicate


        existing = session.query(

            VocabularyDB

        ).filter(

            VocabularyDB.lemma == lemma,

            VocabularyDB.source_language ==
            dictionary["language"]

        ).first()



        if existing:


            return {


                "message":
                    "Already exists",


                "id":
                    existing.id

            }








        vocab = VocabularyDB(


            word=dictionary["word"],


            lemma=lemma,


            source_language=dictionary["language"],


            dictionary_id=dictionary.get(
                "id"
            ),


            cefr=dictionary.get(
                "cefr"
            ),


            source="reading"


        )



        session.add(
            vocab
        )


        session.flush()






        # ===============================
        # Save translations
        # ===============================


        translations = dictionary.get(

            "translations",

            {}

        )



        for lang,text in translations.items():


            if text:


                session.add(

                    VocabularyTranslationDB(

                        vocabulary_id=vocab.id,

                        language=lang,

                        translation=text

                    )

                )







        session.commit()



        return {


            "message":
                "Vocabulary added",


            "id":
                vocab.id,


            "word":
                vocab.word


        }






    except Exception as e:


        session.rollback()


        raise e



    finally:


        session.close()







# =====================================================
# Get vocabulary
# =====================================================


@router.get("")
def get_vocabulary():


    session = SessionLocal()



    try:


        words = session.query(

            VocabularyDB

        ).all()




        result=[]




        for word in words:



            translations={}



            for t in word.translations:


                translations[
                    t.language
                ] = t.translation





            dictionary = word.dictionary




            result.append({


                "id":
                    word.id,


                "word":
                    word.word,


                "lemma":
                    word.lemma,


                "language":
                    word.source_language,


                "definition":

                    dictionary.definition
                    if dictionary
                    else "",


                "pos":

                    dictionary.pos
                    if dictionary
                    else "",



                "cefr":

                    word.cefr,



                "translation":

                    translations.get(
                        "en",
                        ""
                    )


            })



        return result



    finally:


        session.close()