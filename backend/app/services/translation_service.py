import json

from app.ai.factory import get_ai_provider



def _build_translation_prompt(
    sentences: list[str]
) -> str:


    return f"""
Translate the following English sentences into Chinese.

Requirements:
- Keep the original meaning.
- Use natural Chinese.
- Return ONLY valid JSON.
- Keep the same order.

Input sentences:

{json.dumps(
    sentences,
    ensure_ascii=False,
    indent=2
)}


JSON format:

[
    {{
        "sentence_order": 1,
        "translation": "中文翻译"
    }}
]

"""





def _strip_code_fences(
    text: str
) -> str:


    text = text.strip()


    if text.startswith("```"):

        lines = text.splitlines()

        lines = lines[1:]

        if lines[-1].startswith("```"):

            lines = lines[:-1]

        return "\n".join(lines).strip()


    return text





def translate_sentences(
    sentences: list[str]
) -> list[dict]:


    if not sentences:

        return []



    print(
        "[Translation] Starting translation"
    )


    prompt = _build_translation_prompt(
        sentences
    )


    provider = get_ai_provider()


    response = provider.generate(
        prompt
    )


    print(
        "[Translation] Raw response received"
    )



    result = json.loads(
        _strip_code_fences(response)
    )


    print(
        "[Translation] Parsed successfully"
    )


    return result