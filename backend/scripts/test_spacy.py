import sys
from pathlib import Path


# add backend root
sys.path.append(
    str(
        Path(__file__)
        .resolve()
        .parent
        .parent
    )
)


from app.services.word_token_service import tokenize_sentence



sentence = """
Designers can input a few descriptive prompts and instantly visualize complex concepts.
"""


result = tokenize_sentence(sentence)


for word in result:
    print(word)