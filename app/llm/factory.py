import os

from dotenv import load_dotenv

from app.llm.openai_llm import OpenAILLM


load_dotenv()


def get_llm():

    return OpenAILLM(
        api_key=os.getenv(
            "OPENAI_API_KEY"
        )
    )