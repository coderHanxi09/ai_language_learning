import os

from google import genai
from google.genai.errors import APIError

from .provider import AIProvider



class GeminiProvider(AIProvider):


    def __init__(self):

        api_key = os.getenv(
            "GEMINI_API_KEY",
            ""
        ).strip()


        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY not set"
            )


        self.client = genai.Client(
            api_key=api_key
        )


        self.models_cache = None



    # ==================================================
    # Dynamic model discovery
    # ==================================================

    def _get_available_models(self):

        if self.models_cache:
            return self.models_cache



        print(
            "[Gemini] Loading available models..."
        )


        available = []


        try:

            for model in self.client.models.list():


                name = model.name.replace(
                    "models/",
                    ""
                )


                actions = getattr(
                    model,
                    "supported_actions",
                    []
                )


                # only generateContent models

                if (
                    "generateContent"
                    not in actions
                ):
                    continue



                blacklist = [

                    "image",
                    "tts",
                    "audio",
                    "video",
                    "embedding",
                    "robotics",
                    "computer",
                    "nano",
                    "lyria"

                ]


                if any(
                    x in name.lower()
                    for x in blacklist
                ):
                    continue



                available.append(
                    name
                )



        except Exception as exc:

            print(
                "[Gemini] Model discovery failed:",
                exc
            )

            return []



        self.models_cache = (
            self._sort_models(
                available
            )
        )


        print(
            "[Gemini] Selected models:"
        )


        for model in self.models_cache:

            print(
                " -",
                model
            )


        return self.models_cache



    # ==================================================
    # Model ranking
    #
    # Flash Lite
    # >
    # Flash
    # >
    # Pro
    #
    # ==================================================

    def _sort_models(
        self,
        models
    ):


        def score(
            name
        ):

            n = name.lower()



            # ------------------
            # Flash Lite
            # ------------------

            if "flash-lite" in n:


                if "latest" in n:
                    return 0


                if "3.5" in n:
                    return 1


                if "3.1" in n:
                    return 2


                if "2.5" in n:
                    return 3


                if "2.0" in n:
                    return 4



            # ------------------
            # Flash
            # ------------------

            if "flash" in n:


                if "latest" in n:
                    return 10


                if "3.6" in n:
                    return 11


                if "3.5" in n:
                    return 12


                if "3" in n:
                    return 13


                if "2.5" in n:
                    return 14


                if "2.0" in n:
                    return 15



            # ------------------
            # Pro
            # ------------------

            if "pro" in n:

                return 20



            return 100



        return sorted(
            models,
            key=score
        )



    # ==================================================
    # Extract text safely
    # remove thought_signature warning
    # ==================================================

    def _extract_text(
        self,
        response
    ):


        parts = []


        try:

            for candidate in response.candidates:


                for part in candidate.content.parts:


                    text = getattr(
                        part,
                        "text",
                        None
                    )


                    if text:

                        parts.append(
                            text
                        )



        except Exception:


            return None



        return "".join(parts).strip()



    # ==================================================
    # Generate
    # ==================================================

    def generate(
        self,
        prompt: str
    ) -> str:


        models = (
            self._get_available_models()
        )


        if not models:

            raise RuntimeError(
                "No Gemini models available"
            )



        errors = []



        for model in models:


            try:


                print(
                    f"[Gemini] trying {model}"
                )



                response = (
                    self.client
                    .models
                    .generate_content(

                        model=model,

                        contents=prompt,

                        config={

                            "temperature":0.3,

                            "max_output_tokens":800

                        }

                    )
                )



                text = self._extract_text(
                    response
                )


                if not text:

                    raise RuntimeError(
                        "Empty Gemini response"
                    )



                print(
                    f"[Gemini] success {model}"
                )


                return text



            except APIError as exc:


                msg = str(exc)


                print(
                    f"[Gemini] failed {model}"
                )


                errors.append(
                    f"{model}: {msg}"
                )


                # quota exceeded
                # immediately try next model

                if "429" in msg:

                    continue



            except Exception as exc:


                print(
                    f"[Gemini] error {model}: {exc}"
                )


                errors.append(
                    f"{model}: {exc}"
                )



        raise RuntimeError(

            "All Gemini models failed:\n"

            +
            "\n".join(errors)

        )