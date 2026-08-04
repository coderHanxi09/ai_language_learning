import re

from app.ai.factory import get_ai_provider


def split_sentences(text: str) -> list[str]:
    """
    Split text into sentences.
    """

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

    return [
        s.strip()
        for s in sentences
        if s.strip()
    ]


def translate_sentence(sentence: str) -> str:
    """
    Translate one English sentence into Chinese.
    """

    provider = get_ai_provider()

    prompt = f"""
Translate the following English sentence into Simplified Chinese.

Requirements:
- Keep the meaning accurate.
- Do not explain.
- Do not add quotation marks.
- Return ONLY the translated sentence.

Sentence:
{sentence}
"""

    return provider.generate(prompt).strip()