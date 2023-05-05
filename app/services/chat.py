from llama_cpp import Llama
from pygpt4all.models.gpt4all_j import GPT4All_J

from app.core.utils import get_model_info
from app.core import config


class ChatModel:

    @classmethod
    def get_model(cls):
        pass

    @classmethod
    def generate(cls, messages: list, temperature: float = 0.9, top_p: float = 0.9, n: int = 1, stream: bool = False, max_tokens: int = 128, stop: str = "", **kwargs):
        pass

    @classmethod
    def embeddings(cls, text):
        pass


class GPT4AllJBasedModel(ChatModel):
    model = None

    @classmethod
    def generate(cls, messages: list, temperature: float = 0.9, top_p: float = 0.9, n: int = 1, stream: bool = False, max_tokens: int = 128, stop: str = "", **kwargs):
        def text_callback(_):
            pass

        prompt = ""
        for message in messages:
            prompt += f"{message['role']}: {message['content']}\n"
        prompt += "assistant: "

        response = cls.model.generate(prompt, n_predict=max_tokens, seed=-1, n_threads=4,
                                      top_k=40, top_p=top_p, temp=temperature, new_text_callback=text_callback)
        return response

    @classmethod
    def get_model(cls):
        if cls.model is None:
            model_parameters = get_model_info(config.MODEL_ID)
            cls.model = GPT4All_J(model_parameters.get("modelWeightsPath"))

        return cls.model


class LLaMACPPBasedModel(ChatModel):
    model = None

    @classmethod
    def generate(cls, messages: list, temperature: float = 0.9, top_p: float = 0.9, n: int = 1, stream: bool = False, max_tokens: int = 128, stop: str = "", **kwargs):
        response = cls.model.create_chat_completion(
            messages, temperature=temperature, top_p=top_p, stream=stream, stop=[stop], max_tokens=max_tokens)
        return response

    @classmethod
    def get_model(cls):
        if cls.model is None:
            model_parameters = get_model_info(config.MODEL_ID)
            cls.model = Llama(model_path=model_parameters.get("modelWeightsPath"), embedding=True)

        return cls.model

    @classmethod
    def embeddings(cls, text):
        response = cls.model.create_embedding(text)
        return response
