import uuid
from datetime import datetime as dt


def format_chat_response(model_name: str, predictions, usage=None) -> dict:
    if usage is None:
        usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    return {
        "id": uuid.uuid4(),
        "model": model_name,
        "object": "chat.completion",
        "created": int(dt.now().timestamp()),
        "choices": [
            {
                "role": "assistant",
                "index": idx,
                "message": {"role": "assistant", "content": text},
                "finish_reason": "stop",
            }
            for idx, text in enumerate(predictions)
        ],
        "usage": usage,
    }
