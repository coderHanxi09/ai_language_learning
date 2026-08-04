import json
from typing import Optional, List


from nltk.corpus import wordnet as wn


from ..db import SessionLocal
from ..models_db import DictionaryEntryDB





# =========================
# Parse examples
# =========================

def _parse_examples(
    examples
):

    if not examples:

        return []


    if isinstance(
        examples,
        list
    ):

        return examples


    try:

        return json.loads(
            examples
        )


    except Exception:

        return []





# =========================
# Select WordNet meaning
# =========================

def _select_wordnet_synset(
    word
):

    synsets = wn.synsets(
        word
    )


    if not synsets:

        return None



    priority = [

        wn.ADJ,

        wn.NOUN,

        wn.VERB,

        wn.ADV

    ]



    for pos in priority:

        for synset in synsets:

            if synset.pos() == pos:

                return synset



    return synsets[0]





# =========================
# WordNet fallback
# =========================

def _wordnet_lookup(
    word
):


    synset = _select_wordnet_synset(
        word
    )


    if not synset:

        return None



    pos_map = {

        "n": "noun",

        "v": "verb",

        "a": "adjective",

        "r": "adverb"

    }



    return {

        "word": word,

        "lemma":
            synset.lemmas()[0]
            .name()
            .replace("_", " "),


        "definition":
            synset.definition(),


        "pos":
            pos_map.get(
                synset.pos(),
                ""
            ),


        "cefr":
            None,


        "ipa":
            None,


        "examples":
            synset.examples()

    }





# =========================
# Single word lookup
# =========================

def lookup_word(
    word: str
) -> Optional[dict]:


    word = word.strip().lower()


    session = SessionLocal()


    try:


        entry = session.query(
            DictionaryEntryDB
        ).filter(
            DictionaryEntryDB.word.ilike(word)
        ).first()



        if entry:


            return {

                "word":
                    entry.word,

                "lemma":
                    entry.lemma,

                "definition":
                    entry.definition,

                "pos":
                    entry.pos,

                "cefr":
                    entry.cefr,

                "ipa":
                    entry.ipa,

                "examples":
                    _parse_examples(
                        entry.examples
                    )

            }



        result = _wordnet_lookup(
            word
        )


        if not result:

            return None



        new_entry = DictionaryEntryDB(

            word=result["word"],

            lemma=result["lemma"],

            definition=result["definition"],

            pos=result["pos"],

            cefr=result["cefr"],

            ipa=result["ipa"],

            examples=json.dumps(
                result["examples"],
                ensure_ascii=False
            )

        )


        session.add(
            new_entry
        )

        session.commit()



        return result



    finally:

        session.close()





# =========================
# Multiple word lookup
# =========================

def lookup_words(
    words: List[str]
):

    """
    Batch dictionary lookup.
    """

    result = {}



    for word in words:

        data = lookup_word(
            word
        )


        if data:

            result[word] = data



    return result