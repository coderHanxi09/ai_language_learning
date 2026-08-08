import requests



# =====================================================
# Dictionary Provider
# =====================================================


def lookup_german_word(
    word: str
):

    """
    Query external dictionary source.

    Current implementation:
    Free Dictionary API compatible provider.

    Later can replace with:
    - DWDS
    - Wiktionary
    - dict.cc
    """


    try:


        url = (
            "https://api.dictionaryapi.dev/api/v2/entries/en/"
            + word
        )


        response = requests.get(
            url,
            timeout=5
        )


        if response.status_code != 200:

            return None



        data = response.json()



        if not data:

            return None



        item = data[0]



        meanings = item.get(
            "meanings",
            []
        )



        if not meanings:

            return None



        meaning = meanings[0]



        definitions = meaning.get(
            "definitions",
            []
        )



        examples = []


        for d in definitions:


            if d.get("example"):

                examples.append(
                    d["example"]
                )



        return {


            "word":
                word,


            "lemma":
                word.lower(),


            "language":
                "de",


            "pos":
                meaning.get(
                    "partOfSpeech"
                ),


            "cefr":
                None,


            "ipa":
                None,


            "examples":
                examples,


            "translations":
                {

                    "en":
                    definitions[0].get(
                        "definition",
                        ""
                    )

                }

        }



    except Exception as e:


        print(
            "[DICTIONARY PROVIDER ERROR]",
            e
        )


        return None