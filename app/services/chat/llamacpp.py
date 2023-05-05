from llama_cpp import Llama

from app.core import config
from app.core.utils import get_model_info
from app.services.chat.interface import ChatModel


class LLaMACPPBasedModel(ChatModel):
    model = None

    @classmethod
    def generate(
        cls,
        messages: list,
        temperature: float = 0.9,
        top_p: float = 0.9,
        n: int = 1,
        stream: bool = False,
        max_tokens: int = 128,
        stop: str = "",
        **kwargs,
    ):
        response = cls.model.create_chat_completion(
            messages,
            temperature=temperature,
            top_p=top_p,
            stream=stream,
            stop=[stop],
            max_tokens=max_tokens,
        )
        return response

    @classmethod
    def get_model(cls):
        if cls.model is None:
            model_parameters = get_model_info(config.MODEL_ID)
            cls.model = Llama(
                model_path=model_parameters.get("modelWeightsPath"), embedding=True
            )

        return cls.model

    @classmethod
    def embeddings(cls, text):
        response = cls.model.create_embedding(text)
        return response
