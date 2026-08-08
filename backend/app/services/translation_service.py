import json

from app.ai.factory import get_ai_provider




# =====================================================
# Build Translation Prompt
# =====================================================

def _build_translation_prompt(
    sentences: list[str],
    source_language: str,
    target_language: str
) -> str:


    return f"""
You are a professional language translation assistant.

Translate sentences from {source_language}
into {target_language}.

Requirements:

1. Keep the original meaning.
2. Use natural language.
3. Keep the same sentence order.
4. Return ONLY valid JSON.
5. Do not add explanations.


Input sentences:

{json.dumps(
    sentences,
    ensure_ascii=False,
    indent=2
)}



Return format:

[
    {{
        "sentence_order": 1,
        "translation": "translated sentence"
    }}
]

"""





# =====================================================
# Remove Markdown Fence
# =====================================================

def _strip_code_fences(
    text: str
) -> str:


    if not text:

        return ""


    text = text.strip()



    if text.startswith("```"):


        lines = text.splitlines()


        lines = lines[1:]


        if lines and lines[-1].strip().startswith("```"):

            lines = lines[:-1]


        text = "\n".join(lines)



    return text.strip()





# =====================================================
# Translate Sentences
# =====================================================

def translate_sentences(
    sentences: list[str],
    source_language: str = "de",
    target_language: str = "en"
) -> list[dict]:


    """
    Translate multiple sentences.

    Example:

    German -> English

    [
        {
            sentence_order:1,
            translation:"I learn German."
        }
    ]

    """



    if not sentences:

        return []



    print(
        f"[TRANSLATION] {source_language} -> {target_language}"
    )



    prompt = _build_translation_prompt(

        sentences,

        source_language,

        target_language

    )



    provider = get_ai_provider()



    response = provider.generate(
        prompt
    )



    print(
        "[TRANSLATION] Response received"
    )



    cleaned = _strip_code_fences(
        response
    )



    try:

        result = json.loads(
            cleaned
        )


    except Exception as e:


        print(
            "[TRANSLATION ERROR]",
            e
        )


        raise ValueError(
            "Invalid translation JSON"
        )



    return result





# =====================================================
# Single Sentence Translation
# =====================================================

def translate_sentence(
    sentence: str,
    source_language: str = "de",
    target_language: str = "en"
) -> str:


    result = translate_sentences(

        [
            sentence
        ],

        source_language,

        target_language

    )


    if not result:

        return ""



    return result[0]["translation"]