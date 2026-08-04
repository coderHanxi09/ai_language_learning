from typing import List
import re


def split_sentences(
    text: str
) -> List[str]:
    """
    Split article into sentences.
    """

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text.strip()
    )

    return [
        s.strip()
        for s in sentences
        if s.strip()
    ]