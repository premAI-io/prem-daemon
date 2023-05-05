class ChatModel:
    @classmethod
    def get_model(cls):
        pass

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
        pass

    @classmethod
    def embeddings(cls, text):
        pass
