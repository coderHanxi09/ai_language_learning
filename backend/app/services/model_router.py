import os


MODEL_PRIORITY = {
    "simple": [
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash",
    ],

    "normal": [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    ],

    "advanced": [
        "gemini-2.5-pro",
        "gemini-2.5-flash",
    ]
}


def get_models_for_task(task_type: str):
    """
    Return model candidates according to task complexity.

    task_type:
        - simple: reading generation, quiz, examples
        - normal: translation, conversation
        - advanced: analysis, vocabulary graph
    """

    return MODEL_PRIORITY.get(
        task_type,
        MODEL_PRIORITY["simple"]
    )


def get_default_model(task_type: str = "simple"):
    """
    Return first preferred model.
    """

    models = get_models_for_task(task_type)

    return models[0]