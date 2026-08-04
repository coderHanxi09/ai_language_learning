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
            "Try to naturally include these known words if possible: "
            + ", ".join(known_vocabulary)
            + ".\n"
        )


    return f"""
You are an AI language learning assistant.

Generate a reading article for language learners.

Level:
{difficulty}

Topic:
{topic}

{vocab_part}

Requirements:

1. Create an interesting and natural title.
2. Write a reading article suitable for {difficulty} learners.
3. Article length:
   - 3 to 5 paragraphs
   - Around 250-350 words
4. Extract 8-12 useful vocabulary items.
5. Vocabulary should match the article.
6. Return ONLY JSON.
7. Do NOT use markdown.
8. Do NOT add explanations.

Return exactly this JSON structure:

{{
    "title": "Example title",
    "content": "Article content",
    "vocabulary": [
        "word1",
        "word2"
    ]
}}
"""



def _strip_code_fences(
    text: str
) -> str:


    if not text:

        return ""


    text = text.strip()


    # remove ```json
    if text.startswith("```"):


        lines = text.splitlines()


        lines = lines[1:]


        if lines and lines[-1].strip() == "```":

            lines = lines[:-1]


        text = "\n".join(lines)


    return text.strip()



def _extract_json(
    text: str
) -> dict:


    """
    Extract JSON object from AI response.
    """


    text = _strip_code_fences(text)


    try:

        return json.loads(text)


    except json.JSONDecodeError:


        # try extracting {...}

        start = text.find("{")

        end = text.rfind("}")


        if start != -1 and end != -1:


            json_text = text[start:end + 1]


            return json.loads(
                json_text
            )


        raise




def generate_reading(
    topic: str,
    difficulty: str,
    known_vocabulary: List[str]
) -> dict:


    print("[AI] Generating reading...")


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


        print(
            "[AI] Raw response received"
        )


        result = _extract_json(
            response
        )


        # validation

        if not result.get("title"):

            raise ValueError(
                "Missing title"
            )


        if not result.get("content"):

            raise ValueError(
                "Missing content"
            )


        if not isinstance(
            result.get("vocabulary"),
            list
        ):

            result["vocabulary"] = []



        print(
            "[AI] JSON parsed successfully"
        )


        return {


            "title": result["title"],


            "content": result["content"],


            "vocabulary": result["vocabulary"][:12]

        }



    except Exception as exc:


        print(
            "[AI ERROR]",
            exc
        )


        # fallback

        return {


            "title":
                f"{topic.title()} - Reading",


            "content":
                (
                    f"This reading is about {topic}. "
                    f"It is designed for {difficulty} learners."
                ),


            "vocabulary":
                known_vocabulary[:10]

        }