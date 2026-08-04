import json
from typing import List
from app.ai.factory import get_ai_provider



def _build_prompt(
    topic: str,
    difficulty: str,
    known_vocabulary: List[str]
) -> str:


    vocab_part = ""


    if known_vocabulary:

        vocab_part = (
            "Known vocabulary: "
            + ", ".join(known_vocabulary)
            + ".\n"
        )



    return (

        "Generate a reading article for language learners.\n"

        f"Difficulty level: {difficulty}.\n"

        f"Topic: {topic}.\n"

        f"{vocab_part}"


        "Requirements:\n"

        "- Create a suitable title.\n"

        "- Write a natural reading article.\n"

        "- Provide useful vocabulary.\n"

        "- Return ONLY valid JSON.\n\n"


        "JSON format:\n"

        "{\n"

        '  "title": "...",\n'

        '  "content": "...",\n'

        '  "vocabulary": ["word1","word2"]\n'

        "}"

    )



def _strip_code_fences(
    text:str
)->str:


    text=text.strip()


    if not text.startswith("```"):

        return text


    lines=text.splitlines()


    if lines:

        lines=lines[1:]


    if lines and lines[-1].startswith("```"):

        lines=lines[:-1]


    return "\n".join(lines).strip()



def generate_reading(
    topic: str,
    difficulty: str,
    known_vocabulary: List[str]
) -> dict:



    prompt = _build_prompt(
        topic,
        difficulty,
        known_vocabulary
    )


    try:


        provider = get_ai_provider()


        response = provider.generate(
            prompt
        )


        return json.loads(
            _strip_code_fences(response)
        )



    except Exception as exc:


        print(
            "[AI fallback]",
            exc
        )


        return {

            "title":
                f"{topic.title()} - generated reading",


            "content":
                (
                    f"This is a {difficulty} "
                    f"level reading about {topic}. "
                    "AI generation failed."
                ),


            "vocabulary":
                known_vocabulary[:10]

        }