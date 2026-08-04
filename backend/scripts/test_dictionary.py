import sys
from pathlib import Path


sys.path.append(
    str(
        Path(__file__)
        .parent
        .parent
    )
)


from app.services.dictionary_service import lookup_word



result = lookup_word(
    "environment"
)


print(result)