# ai-box

> Prem: A Privacy-Centric Open-Source AI Cloud Infrastructure Powered by Nostr. A cutting-edge, open-source AI platform designed with privacy at its core. Leveraging state-of-the-art Large Language Models (LLMs), Prem provides a secure and flexible environment for self-hosting AI models or utilizing our privacy-focused cloud infrastructure.

## Getting Started

### Run the backend with docker-compose

```bash
docker-compose up --build -d
```

### Run the backend with Docker

```bash
docker run -d -v $(pwd)/models:/usr/src/app/models -p 8002:8002 --name ai_box filippopedrazzini/the_ai_box:latest 
```

### LLMs

Models available to download

- GPT4ALL 7B
- GPT4ALL 7B unfiltered
- Vicuna 7B rev 1 
- Vicuna 13B rev 1
- ggml-gpt4all-j-v1.3-groovy
- ggml-gpt4all-j-v1.2-jazzy
- ggml-gpt4all-l13b-snoozy
- ggml-gpt4all-j-v1.1-breezy
- ggml-gpt4all-j
- ggml-vicuna-7b-1.1-q4_2
- ggml-vicuna-13b-1.1-q4_2

### Speech

- Whisper

### Images

- Stable diffusion