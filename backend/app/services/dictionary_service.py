import nltk
from nltk.corpus import wordnet
from wordfreq import zipf_frequency
import eng_to_ipa as ipa


# =========================
# POS mapping
# =========================

WORDNET_POS_MAP = {

    "n": "noun",

    "v": "verb",

    "a": "adjective",

    "r": "adverb"

}



# =========================
# CEFR estimation
# =========================

def estimate_cefr(word: str):

    """
    Estimate CEFR level using word frequency.

    Higher zipf frequency:
    easier word.
    """


    freq = zipf_frequency(
        word,
        "en"
    )


    if freq >= 6:

        return "A1"


    elif freq >= 5:

        return "A2"


    elif freq >= 4:

        return "B1"


    elif freq >= 3:

        return "B2"


    elif freq >= 2:

        return "C1"


    else:

        return "C2"





# =========================
# Lemma
# =========================

def get_lemma(
    word: str
):


    synsets = wordnet.synsets(
        word
    )


    if not synsets:

        return word



    lemma = synsets[0].lemmas()[0].name()


    return lemma.replace(
        "_",
        " "
    )





# =========================
# POS
# =========================

def get_pos(
    word: str
):


    synsets = wordnet.synsets(
        word
    )


    if not synsets:

        return None



    pos = synsets[0].pos()


    return WORDNET_POS_MAP.get(
        pos
    )





# =========================
# Definition
# =========================

def get_definition(
    word: str
):


    synsets = wordnet.synsets(
        word
    )


    if not synsets:

        return None



    return synsets[0].definition()





# =========================
# Examples
# =========================

def get_examples(
    word: str
):


    synsets = wordnet.synsets(
        word
    )


    if not synsets:

        return []



    return synsets[0].examples()





# =========================
# IPA
# =========================

def get_ipa(
    word: str
):


    try:

        result = ipa.convert(
            word
        )


        if result:

            return result



    except Exception:

        pass



    return None





# =========================
# Main lookup
# =========================

def lookup_word(
    word: str
):


    word = word.lower().strip()



    lemma = get_lemma(
        word
    )


    definition = get_definition(
        word
    )


    pos = get_pos(
        word
    )


    examples = get_examples(
        word
    )


    pronunciation = get_ipa(
        word
    )


    cefr = estimate_cefr(
        word
    )



    return {

        "word": word,

        "lemma": lemma,

        "definition": definition,

        "pos": pos,

        "cefr": cefr,

        "ipa": pronunciation,

        "examples": examples

    }