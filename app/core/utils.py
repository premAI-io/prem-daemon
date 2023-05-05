import logging
import os
import ssl
import urllib.request

from tqdm import tqdm

from app.core import config

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

logger = logging.getLogger(__name__)


def get_models_info() -> dict:
    return {
        "data": [
            {
                "id": "ggml-vicuna-7b-1.1-q4_2",
                "name": "Vicuna 7B 1.1 Q4",
                "maxLength": 12000,
                "tokenLimit": 4000,
                "description": "Vicuna 7B 1.1 Q4",
                "modelWeightsName": "ggml-vicuna-7b-1.1-q4_2.bin",
                "modelWeightsPath": f"{config.MODEL_WEIGHTS_DIR}/ggml-vicuna-7b-1.1-q4_2.bin",
                "modelWeightsUrl": "https://prem-models.s3.eu-central-1.amazonaws.com/ggml-vicuna-7b-1.1-q4_2.bin",
                "modelWeightsSize": 4212859520,
                "modelTypes": ["chat", "embeddings"],
                "modelDevice": "m1",
            },
            {
                "id": "gpt4all-lora-quantized-ggml",
                "name": "GPT4ALL-Lora Quantized GGML",
                "maxLength": 12000,
                "tokenLimit": 4000,
                "description": "GPT4ALL-Lora Quantized GGML",
                "modelWeightsName": "gpt4all-lora-quantized-ggml.bin",
                "modelWeightsPath": f"{config.MODEL_WEIGHTS_DIR}/gpt4all-lora-quantized-ggml.bin",
                "modelWeightsUrl": "https://prem-models.s3.eu-central-1.amazonaws.com/gpt4all-lora-quantized-ggml.bin",
                "modelWeightsSize": 4212864640,
                "modelTypes": ["chat", "embeddings"],
                "modelDevice": "m1",
            },
        ]
    }


def get_model_info(model_id: str) -> dict:
    for model in get_models_info()["data"]:
        if model["id"] == model_id:
            return model
    raise ValueError("Model id not supported.")


def check_model_ready():
    model_parameters = get_model_info(config.MODEL_ID)

    if not os.path.exists(model_parameters.get("modelWeightsPath")):
        return False, 0
    actual_size = os.path.getsize(model_parameters.get("modelWeightsPath"))
    percentage = int((actual_size / model_parameters.get("modelWeightsSize")) * 100)
    return actual_size == model_parameters.get("modelWeightsSize"), percentage


def download_model():
    model_parameters = get_model_info(config.MODEL_ID)

    logger.info(
        f"Downloading model weights in path {model_parameters.get('modelWeightsPath')}"
    )
    with tqdm(
        unit="B",
        unit_scale=True,
        miniters=1,
        desc=model_parameters.get("modelWeightsUrl").split("/")[-1],
    ) as progress_bar:
        with urllib.request.urlopen(
            model_parameters.get("modelWeightsUrl"),
            context=ssl_context,
        ) as response, open(model_parameters.get("modelWeightsPath"), "wb") as out_file:
            while True:
                chunk = response.read(8192)
                if not chunk:
                    break
                out_file.write(chunk)
                progress_bar.update(len(chunk))
    logger.info(
        f"Downloaded model weights in path {model_parameters.get('modelWeightsPath')}"
    )


def load_model():
    if config.MODEL_ID in ["gpt4all-lora-quantized-ggml", "ggml-vicuna-7b-1.1-q4_2"]:
        from app.services.chat.llamacpp import LLaMACPPBasedModel

        LLaMACPPBasedModel.get_model()
    else:
        raise ValueError("Model id not supported.")


def get_model():
    if config.MODEL_ID in ["gpt4all-lora-quantized-ggml", "ggml-vicuna-7b-1.1-q4_2"]:
        from app.services.chat.llamacpp import LLaMACPPBasedModel as model

        return model
    else:
        raise ValueError("Model id not supported.")
