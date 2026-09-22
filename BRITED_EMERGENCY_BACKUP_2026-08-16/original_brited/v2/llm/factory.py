from .openai_client import OpenAILLM


class LLMFactory:

    @staticmethod
    def create():

        return OpenAILLM()
    