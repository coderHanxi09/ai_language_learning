import spacy

from functools import lru_cache




@lru_cache(maxsize=5)
def get_nlp(language:str):


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







def analyze_sentence(
    sentence:str,
    language:str="de"
):


    nlp = get_nlp(
        language
    )


    doc = nlp(
        sentence
    )


    result=[]


    for token in doc:


        if token.is_space:

            continue



        if token.is_punct:

            continue



        # 保留：
        # AfD
        # Verbotsverfahrens
        # 1000
        # KI-Modelle

        word = token.text.strip()



        if not word:

            continue



        result.append(

            {

                "word":
                    word,


                "lemma":
                    token.lemma_.lower(),


                "pos":
                    token.pos_

            }

        )


    return result







def tokenize_sentence(
    sentence:str,
    language:str="de"
):


    return analyze_sentence(
        sentence,
        language
    )







def normalize_word(
    word:str,
    language:str="de"
):


    nlp=get_nlp(
        language
    )


    doc=nlp(
        word
    )


    if len(doc)==0:

        return word.lower()



    return doc[0].lemma_.lower()