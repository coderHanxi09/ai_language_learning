from sqlalchemy.orm import Session

from app.models_db import ReadingWordDB
from app.services.word_token_service import tokenize_sentence
from app.services.dictionary_service import lookup_word


def process_sentence_words(
    db: Session,
    reading_id: int,
    sentence: str
):
    """
    Process one sentence:
    tokenize -> lemma -> pos -> dictionary -> save
    """

    words = tokenize_sentence(sentence)

    saved_words = []


    for item in words:

        word = item["word"]
        lemma = item["lemma"]
        pos = item["pos"]


        dictionary = lookup_word(lemma)


        reading_word = ReadingWordDB(
            reading_id=reading_id,
            word=word,
            lemma=lemma,
            pos=pos,

            definition=(
                dictionary["definition"]
                if dictionary
                else None
            ),

            ipa=(
                dictionary["ipa"]
                if dictionary
                else None
            ),

            cefr=(
                dictionary["cefr"]
                if dictionary
                else None
            )
        )


        db.add(reading_word)

        saved_words.append(reading_word)


    db.commit()


    return saved_words