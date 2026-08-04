import spacy


# =========================
# Load spaCy model
# =========================

nlp = spacy.load(
    "en_core_web_sm"
)



# =========================
# Tokenize sentence
# =========================

def tokenize_sentence(
    sentence: str
):

    doc = nlp(sentence)


    tokens = []


    for token in doc:

        # ignore punctuation
        if not token.is_punct:

            tokens.append(
                token.text
            )


    return tokens





# =========================
# Normalize word
# =========================

def normalize_word(
    word: str
):

    doc = nlp(word)


    if len(doc) == 0:
        return word.lower()


    return doc[0].lemma_.lower()