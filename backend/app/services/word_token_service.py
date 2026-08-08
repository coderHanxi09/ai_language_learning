import spacy
from functools import lru_cache




# =====================================================
# Load NLP model by language
# =====================================================

@lru_cache(maxsize=5)
def get_nlp(
    language: str
):

    """
    Load spaCy model.

    Supported:

    de -> German
    en -> English

    """


    if language == "de":

        return spacy.load(
            "de_core_news_sm"
        )


    elif language == "en":

        return spacy.load(
            "en_core_web_sm"
        )


    else:

        raise ValueError(
            f"Unsupported language: {language}"
        )






# =====================================================
# Analyze sentence
# =====================================================

def analyze_sentence(
    sentence: str,
    language: str = "de"
):

    """
    Analyze sentence.

    Example German:

    Entscheidungsmöglichkeiten

    ->
    
    {
        word:
        lemma:
        pos:
    }

    """


    nlp = get_nlp(
        language
    )


    doc = nlp(
        sentence
    )


    result = []


    for token in doc:


        # ignore punctuation
        if token.is_punct:

            continue


        # ignore spaces
        if token.is_space:

            continue



        if not token.is_alpha:

            continue



        result.append(

            {

                "word":
                    token.text,


                "lemma":
                    token.lemma_.lower(),


                "pos":
                    token.pos_

            }

        )


    return result







# =====================================================
# Tokenize sentence
# =====================================================

def tokenize_sentence(
    sentence: str,
    language: str = "de"
):

    """
    Return analyzed tokens.

    Used by reading pipeline.

    """


    return analyze_sentence(

        sentence,

        language

    )







# =====================================================
# Normalize word
# =====================================================

def normalize_word(
    word: str,
    language: str = "de"
):

    """
    Convert word to lemma.

    Example:

    German:

    gegangen -> gehen

    Wörter -> wort


    English:

    running -> run

    """


    nlp = get_nlp(
        language
    )


    doc = nlp(
        word
    )


    if not doc:

        return word.lower()



    return doc[0].lemma_.lower()