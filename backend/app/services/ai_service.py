import json
from typing import List


from app.ai.factory import get_ai_provider





# =====================================================
# Build prompt
# =====================================================


def _build_prompt(
    topic: str,
    difficulty: str,
    source_language: str,
    translation_language: str,
    known_vocabulary: List[str]
) -> str:


    vocab_part = ""


    if known_vocabulary:

        vocab_part = f"""
Try to naturally include these vocabulary items:

{", ".join(known_vocabulary)}

"""



    return f"""

You are an AI language learning assistant.


Generate a reading article for language learners.


Learning mode:

Source language:
{source_language}


Translation language:
{translation_language}


Level:
{difficulty}


Topic:
{topic}



{vocab_part}



Requirements:


1. Generate the article in the source language.

2. The article should be suitable for {difficulty} learners.

3. Create a natural and interesting title.

4. Article length:
- 3 to 5 paragraphs
- Around 250-350 words


5. Extract 8-12 useful vocabulary words from the article.

6. Vocabulary should be in the source language.

7. Return ONLY JSON.

8. Do NOT use markdown.

9. Do NOT add explanations.



Return exactly this structure:


{{
    "title": "Article title",

    "content": "Article content",

    "vocabulary": [

        "word1",

        "word2"

    ]
}}


"""






# =====================================================
# Remove markdown fences
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



        if lines and lines[-1].strip() == "```":

            lines = lines[:-1]



        text = "\n".join(lines)



    return text.strip()






# =====================================================
# Extract JSON
# =====================================================


def _extract_json(
    text: str
) -> dict:


    text = _strip_code_fences(
        text
    )



    try:

        return json.loads(text)



    except json.JSONDecodeError:



        start = text.find("{")

        end = text.rfind("}")



        if start != -1 and end != -1:


            return json.loads(

                text[start:end+1]

            )



        raise






# =====================================================
# Generate Reading
# =====================================================


def generate_reading(
    topic: str,
    difficulty: str,
    source_language: str,
    translation_language: str,
    known_vocabulary: List[str]
) -> dict:



    print(
        "[AI] Generating reading"
    )


    prompt = _build_prompt(

        topic,

        difficulty,

        source_language,

        translation_language,

        known_vocabulary

    )



    try:


        provider = get_ai_provider()



        response = provider.generate(

            prompt

        )



        print(
            "[AI] Response received"
        )



        result = _extract_json(

            response

        )



        if not result.get("title"):

            raise ValueError(
                "Missing title"
            )



        if not result.get("content"):

            raise ValueError(
                "Missing content"
            )



        vocabulary = result.get(
            "vocabulary",
            []
        )



        if not isinstance(
            vocabulary,
            list
        ):

            vocabulary = []



        return {


            "title":
                result["title"],



            "content":
                result["content"],



            "vocabulary":
                vocabulary[:12]

        }



    except Exception as e:


        print(
            "[AI ERROR]",
            e
        )



        # fallback

        return {


            "title":
                f"{topic.title()} Reading",



            "content":

                (
                    f"Dieser Text handelt von {topic}. "
                    "Er wurde für Sprachlernende erstellt."
                )

                if source_language == "de"

                else

                (
                    f"This reading is about {topic}. "
                    "It was created for language learners."
                ),



            "vocabulary":

                known_vocabulary[:10]

        }