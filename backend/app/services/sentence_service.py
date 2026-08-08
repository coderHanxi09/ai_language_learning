import re

from app.ai.factory import get_ai_provider



def split_sentences(text: str) -> list[str]:
    """
    Split German / English sentences safely.

    Handles:
    - numbers: 1.000
    - abbreviations
    - normal punctuation
    """


    text = text.strip()


    # protect numbers
    text = re.sub(
        r"(\d)\.(\d)",
        r"\1<DOT>\2",
        text
    )


    # protect common abbreviations

    abbreviations = [
        "z.B.",
        "d.h.",
        "u.a.",
        "Dr.",
        "Prof.",
        "Nr."
    ]


    for abbr in abbreviations:

        text = text.replace(
            abbr,
            abbr.replace(
                ".",
                "<DOT>"
            )
        )


    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )


    result=[]


    for sentence in sentences:

        sentence = sentence.replace(
            "<DOT>",
            "."
        )


        sentence = sentence.strip()


        if sentence:

            result.append(
                sentence
            )


    return result





def translate_sentence(sentence: str) -> str:
    """
    Translate one sentence.
    """

    provider = get_ai_provider()


    prompt = f"""
Translate the following German sentence into English.

Requirements:
- Keep the meaning accurate.
- Do not explain.
- Return ONLY the translation.

Sentence:
{sentence}
"""


    return provider.generate(
        prompt
    ).strip()