import spacy


nlp = spacy.load(
    "en_core_web_sm"
)


def analyze_sentence(sentence):

    doc = nlp(sentence)


    result=[]


    for token in doc:

        if token.is_alpha:

            result.append(
                {
                    "word":token.text,
                    "lemma":token.lemma_,
                    "pos":token.pos_
                }
            )


    return result