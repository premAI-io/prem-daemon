import json
import logging
import time
import uuid
from datetime import datetime as dt

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


class ChatCompletionInput(BaseModel):
    model: str | None
    messages: list[dict]
    temperature: float = 1.0
    top_p: float = 1.0
    n: int = 1
    stream: bool = False
    stop: str | list | None = ""
    max_tokens: int = 7
    presence_penalty: float = 0.0
    frequence_penalty: float = 0.0
    logit_bias: dict | None = {}
    user: str = ""


class ChatCompletionResponse(BaseModel):
    id: str = uuid.uuid4()
    model: str
    object: str = "chat.completion"
    created: int = int(dt.now().timestamp())
    choices: list[dict]
    usage: dict = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}


class EmbeddingsInput(BaseModel):
    model: str
    input: str
    user: str = ""


class EmbeddingObject(BaseModel):
    object: str = "embedding"
    index: int = 0
    embedding: list[float]


class EmbeddingUsage(BaseModel):
    prompt_tokens: int = 0
    total_tokens: int = 0


class EmbeddingsResponse(BaseModel):
    object: str = "list"
    data: list[EmbeddingObject]
    model: str = ""
    usage: EmbeddingUsage


class HealthResponse(BaseModel):
    status: bool


router = APIRouter()


@router.get("/", response_model=HealthResponse)
async def health():
    return HealthResponse(status=True)


async def generate_chunk_based_response():
    chunks = [
        {
            "id": "chat",
            "object": "chat.completion.chunk",
            "created": 1680533987,
            "model": "gpt-4-all",
            "choices": [
                {"delta": {"content": "Hello "}, "index": 0, "finish_reason": None}
            ],
        },
        {
            "id": "chat",
            "object": "chat.completion.chunk",
            "created": 1680533987,
            "model": "gpt-4-all",
            "choices": [
                {"delta": {"content": "World"}, "index": 0, "finish_reason": None}
            ],
        },
    ]
    for chunk in chunks:
        yield f"event: completion\ndata: {json.dumps(chunk)}\n\n"
        time.sleep(1)
    yield "event: done\ndata: [DONE]\n\n"


@router.post("/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(body: ChatCompletionInput):
    if body.stream:
        return StreamingResponse(
            generate_chunk_based_response(), media_type="text/event-stream"
        )
    return {
        "id": str(uuid.uuid4()),
        "model": "chat-mock",
        "object": "chat.completion",
        "created": int(dt.now().timestamp()),
        "choices": [
            {
                "role": "assistant",
                "index": idx,
                "message": {"role": "assistant", "content": text},
                "finish_reason": "stop",
            }
            for idx, text in enumerate(["Hello world"])
        ],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }


@router.post("/embeddings", response_model=EmbeddingsResponse)
async def embeddings(body: EmbeddingsInput):
    return EmbeddingsResponse(
        object="list",
        data=[EmbeddingObject(embedding=[0.1, 0.1, 0.1])],
        model=body.model,
        usage=EmbeddingUsage(),
    )


def get_application() -> FastAPI:
    application = FastAPI(title="Prem Mocks", debug=True, version="0.0.1")
    application.include_router(router, prefix="/api/v1")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
