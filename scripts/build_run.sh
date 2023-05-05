
docker buildx build --platform linux/amd64 --build-arg="MODEL_ID=gpt4all-lora-quantized-ggml" -t ghcr.io/premai-io/prem-chat-gpt4all-lora-quantized-ggml-m1:latest -f ./docker/m1/chat/Dockerfile .
docker buildx build --platform linux/amd64 --build-arg="MODEL_ID=gpt4all-j-v1.3-groovy" -t ghcr.io/premai-io/prem-chat-gpt4all-j-v1.3-groovy-m1:latest -f ./docker/m1/chat/Dockerfile .




docker run -d -it -v $(pwd)/models:/usr/src/app/models -p 8000:8000 --platform linux/amd64 --name prem_chat ghcr.io/premai-io/prem-chat-ggml-vicuna-7b-1.1-q4_2-m1:latest bash
docker run -it -v $(pwd)/models:/usr/src/app/models --platform linux/amd64 python:3.10-slim-bullseye bash








docker run --rm -it -p 8000:8000 -v $(pwd)/models:/models -eMODEL=/models/ggml-vicuna-7b-1.1-q4_2.bin ghcr.io/abetlen/llama-cpp-python:latest bash
docker run --rm -it -p 8000:8000 -v $(pwd)/models:/models -eMODEL=/models/ggml-vicuna-7b-1.1-q4_2.bin ghcr.io/abetlen/llama-cpp-python:latest@sha256:c80b492d83e39df8196980741676a6942e76a3923be48c72b0ebf403d67849d6 bash


from llama_cpp import Llama
llm = Llama(model_path="./models/ggml-vicuna-7b-1.1-q4_2.bin")






docker run -it -v $(pwd)/models:/usr/src/app/models --platform linux/arm64 python:3.10-slim-bullseye bash

model = Model('./models/gpt4all-j-v1.3-groovy.bin')
