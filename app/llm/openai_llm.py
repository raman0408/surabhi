from openai import OpenAI

from app.llm.base import BaseLLM


class OpenAILLM(BaseLLM):

    def __init__(
        self,
        api_key,
        model="gpt-5.4-mini"
    ):
        self.client = OpenAI(
            api_key=api_key
        )

        self.model = model

    def invoke(
        self,
        prompt: str
    ) -> str:

        response = self.client.responses.create(
            model=self.model,
            input=prompt
        )

        return response.output_text