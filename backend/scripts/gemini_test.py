#!/usr/bin/env python3

import json
import os
from pathlib import Path

from google import genai
from google.genai.errors import APIError



def load_env(path: Path) -> dict[str, str]:

    data = {}

    if not path.exists():
        return data


    for line in path.read_text().splitlines():

        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" in line:

            key, value = line.split("=", 1)

            data[key.strip()] = (
                value
                .strip()
                .strip('"')
                .strip("'")
            )

    return data



def get_models(env: dict[str, str]) -> list[str]:

    """
    Read model priority from .env

    Example:
    GEMINI_MODELS=
        gemini-2.5-flash,
        gemini-2.0-flash
    """


    models = (
        os.getenv("GEMINI_MODELS")
        or env.get("GEMINI_MODELS")
    )


    if models:

        return [
            m.strip()
            for m in models.split(",")
            if m.strip()
        ]


    # default fallback order
    return [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
    ]



def main():


    env = load_env(
        Path(__file__).resolve().parents[1] / ".env"
    )


    api_key = (
        os.getenv("GEMINI_API_KEY")
        or env.get("GEMINI_API_KEY")
    )


    if not api_key:

        print(
            "[gemini_test] GEMINI_API_KEY not found"
        )

        return



    models = get_models(env)


    prompt = """
Generate a short B2-level reading about climate change.

Return ONLY valid JSON:

{
    "title": "...",
    "content": "...",
    "vocabulary": [
        "word1",
        "word2"
    ]
}
"""


    client = genai.Client(
        api_key=api_key
    )


    errors = []


    payload = None



    for model_name in models:

        print(
            f"[gemini_test] trying model: {model_name}"
        )


        try:

            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config={
                    "temperature": 0.2,
                    "max_output_tokens": 500,
                },
            )


            payload = {

                "status": "ok",

                "model": model_name,

                "text": response.text,

            }


            print(
                f"[gemini_test] success: {model_name}"
            )


            break



        except APIError as exc:


            print(
                f"[gemini_test] failed: {model_name}"
            )


            errors.append(
                f"{model_name}: {exc}"
            )



        except Exception as exc:


            print(
                f"[gemini_test] unexpected error: {model_name}"
            )


            errors.append(
                f"{model_name}: {exc}"
            )



    if payload is None:

        payload = {

            "status": "error",

            "errors": errors

        }



    output = Path(
        "/tmp/gemini_test_output.json"
    )


    output.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2
        )
    )


    print(
        f"[gemini_test] wrote {output}"
    )



if __name__ == "__main__":
    main()