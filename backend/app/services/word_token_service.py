import nltk

from functools import lru_cache



# =====================================================
# Initialize NLTK resources
# =====================================================

@lru_cache(maxsize=1)
def init_nltk():


    resources = [

        "punkt",

        "punkt_tab",

        "averaged_perceptron_tagger_eng"

    ]



    for resource in resources:


        try:

            nltk.data.find(resource)


        except LookupError:


            nltk.download(

                resource,

                quiet=True

            )








# =====================================================
# Simple lemma dictionary
# =====================================================

EN_LEMMA_MAP = {


    "am":
        "be",

    "is":
        "be",

    "are":
        "be",

    "was":
        "be",

    "were":
        "be",


    "children":
        "child",

    "mice":
        "mouse",


    "went":
        "go",

    "gone":
        "go",


}






# =====================================================
# German simple normalization
# =====================================================


def german_lemma(word:str):


    w = word.lower()



    # plural endings

    endings = [

        "en",

        "er",

        "e",

        "n",

        "s"

    ]



    for ending in endings:


        if (

            len(w)>5

            and

            w.endswith(ending)

        ):


            return w[:-len(ending)]



    return w







# =====================================================
# English simple lemma
# =====================================================


def english_lemma(word:str):


    w = word.lower()



    if w in EN_LEMMA_MAP:

        return EN_LEMMA_MAP[w]



    # plural

    if (

        len(w)>4

        and

        w.endswith("ies")

    ):


        return w[:-3]+"y"



    if (

        len(w)>4

        and

        w.endswith("s")

    ):


        return w[:-1]



    # verbs

    if (

        len(w)>5

        and

        w.endswith("ing")

    ):


        return w[:-3]



    if (

        len(w)>5

        and

        w.endswith("ed")

    ):


        return w[:-2]



    return w







# =====================================================
# POS tagging
# =====================================================


def get_pos(

    tokens,

    language="en"

):


    if language=="en":


        tagged = nltk.pos_tag(

            tokens

        )


        return {

            word:pos

            for word,pos in tagged

        }



    # NLTK has no good German POS model

    return {

        word:None

        for word in tokens

    }









# =====================================================
# Analyze sentence
# =====================================================


def analyze_sentence(

    sentence:str,

    language:str="de"

):


    init_nltk()



    tokens = nltk.word_tokenize(

        sentence,

        language=(

            "german"

            if language=="de"

            else

            "english"

        )

    )




    words=[]



    clean_tokens=[]




    for token in tokens:


        # remove punctuation only

        if token.isalpha() or "-" in token:


            clean_tokens.append(

                token

            )



        # keep numbers

        elif token.isdigit():


            clean_tokens.append(

                token

            )







    pos_map=get_pos(

        clean_tokens,

        language

    )







    for token in clean_tokens:



        if language=="en":


            lemma = english_lemma(

                token

            )


        else:


            lemma = german_lemma(

                token

            )





        words.append(

            {


                "word":

                    token,



                "lemma":

                    lemma,



                "pos":

                    pos_map.get(

                        token

                    )



            }

        )





    return words









# =====================================================
# Alias
# =====================================================


def tokenize_sentence(

    sentence:str,

    language:str="de"

):


    return analyze_sentence(

        sentence,

        language

    )









# =====================================================
# Normalize word
# =====================================================


def normalize_word(

    word:str,

    language:str="de"

):


    if language=="en":


        return english_lemma(

            word

        )



    return german_lemma(

        word

    )