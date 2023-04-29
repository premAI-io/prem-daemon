from fastapi import APIRouter

from app.core import config
from app.core.utils import get_model
from app.models.chat import ChatCompletionInput
from app.models.utils import format_chat_response

router = APIRouter()


@router.post("/chat/completions")
async def chat_completions(body: ChatCompletionInput):
    predictions = get_model().generate(messages=body.messages, temperature=body.temperature, top_p=body.top_p, n=body.n, stream=body.stream, max_tokens=body.max_tokens,
                                       stop=body.stop, presence_penalty=body.presence_penalty, frequence_penalty=body.frequence_penalty, logit_bias=body.logit_bias)

    return format_chat_response(model_name=config.MODEL_ID, predictions=predictions)
