import logging

logger = logging.getLogger(__name__)


def get_services_info() -> dict:
    return {
        "data": [
            {
                "id": "vicuna-7b-q4",
                "name": "Vicuna 7B Q4",
                "icon": "",
                "maxLength": 12000,
                "tokenLimit": 4000,
                "description": "Vicuna 7B Q4",
                "modelWeightsName": "vicuna-7b-q4.bin",
                "modelWeightsSize": 4212859520,
                "modelTypes": ["chat", "embeddings"],
                "modelDevice": "m1",
                "modelMemoryRequirements": "8gb",
                "dockerImage": "ghcr.io/premai-io/prem-chat-vicuna-7b-q4-m1:latest",
            },
            {
                "id": "gpt4all-lora-q4",
                "name": "GPT4ALL-Lora Q4",
                "icon": "",
                "maxLength": 12000,
                "tokenLimit": 4000,
                "description": "GPT4ALL-Lora Q4",
                "modelWeightsName": "gpt4all-lora-q4.bin",
                "modelWeightsSize": 4212864640,
                "modelTypes": ["chat", "embeddings"],
                "modelDevice": "m1",
                "dockerImage": "ghcr.io/premai-io/prem-chat-gpt4all-lora-q4-m1:latest",
            },
        ]
    }


def get_service_info(service_id: str) -> dict:
    for service in get_services_info()["data"]:
        if service["id"] == service_id:
            return service
    raise ValueError("Service id not supported.")
