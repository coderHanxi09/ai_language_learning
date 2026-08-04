import os

from dotenv import load_dotenv

from app.ai.gemini_provider import GeminiProvider
from app.ai.local_provider import LocalLLMProvider


load_dotenv()


def get_ai_provider():

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )


    if api_key:

        print(
            "[AI] Using Gemini Provider"
        )

        return GeminiProvider()


    print(
        "[AI] Using Local LLM Provider"
    )

    return LocalLLMProvider()