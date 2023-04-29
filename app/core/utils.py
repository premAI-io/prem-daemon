import os
import logging
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
                "id": "gpt4all-j-v1.3-groovy",
                "name": "GPT-4-ALL-J v1.3 Groovy",
                "maxLength": 12000,
                "tokenLimit": 4000,
                "description": "GPT-4-ALL-J v1.3 Groovy is a 1.3B parameter model trained on the Groovy dataset.",
                "modelWeightsName": "ggml-gpt4all-j-v1.3-groovy.bin",
                "modelWeightsPath": f"{config.MODEL_WEIGHTS_DIR}/ggml-gpt4all-j-v1.3-groovy.bin",
                "modelWeightsUrl": "https://prem-models.s3.eu-central-1.amazonaws.com/ggml-gpt4all-j-v1.3-groovy.bin",
                "modelWeightsSize": 3785248281,
                "modelType": "chat"
            }
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

    logger.info(f"Downloading model weights in path {model_parameters.get('modelWeightsPath')}")
    with tqdm(
        unit="B", unit_scale=True, miniters=1, desc=model_parameters.get('modelWeightsUrl').split("/")[-1]
    ) as progress_bar:
        with urllib.request.urlopen(
            model_parameters.get('modelWeightsUrl'),
            context=ssl_context,
        ) as response, open(model_parameters.get("modelWeightsPath"), "wb") as out_file:
            while True:
                chunk = response.read(8192)
                if not chunk:
                    break
                out_file.write(chunk)
                progress_bar.update(len(chunk))
    logger.info(f"Downloaded model weights in path {model_parameters.get('modelWeightsPath')}")


def load_model():
    if config.MODEL_ID in ["gpt4all-j-v1.3-groovy"]:
        from app.services.text import GPT4AllBasedModel
        GPT4AllBasedModel.get_model()
    else:
        raise ValueError("Model id not supported.")


def get_model():
    if config.MODEL_ID in ["gpt4all-j-v1.3-groovy"]:
        from app.services.text import GPT4AllBasedModel as model
        return model
    else:
        raise ValueError("Model id not supported.")
