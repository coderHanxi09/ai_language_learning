from .provider import AIProvider



class LocalLLMProvider(AIProvider):


    def __init__(
        self,
        model_name="local-model"
    ):

        self.model_name = model_name



    def generate(
        self,
        prompt:str
    )->str:


        # TODO:
        # connect HuggingFace
        # or Ollama


        return (
            "Local model response"
        )