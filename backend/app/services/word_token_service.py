import re


def tokenize_sentence(sentence: str):
    """
    Split sentence into words.

    Example:
    "AI is changing the world."
    =>
    ["AI", "is", "changing", "the", "world"]
    """


    words = re.findall(
        r"\b[a-zA-Z]+(?:'[a-zA-Z]+)?\b",
        sentence
    )


    return words





def normalize_word(word: str):
    """
    Normalize word for dictionary lookup.
    """

    return word.lower()