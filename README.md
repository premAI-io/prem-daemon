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
