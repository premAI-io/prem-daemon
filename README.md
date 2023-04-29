# ai-box

> Prem: A Privacy-Centric Open-Source AI Cloud Infrastructure Powered by Nostr. A cutting-edge, open-source AI platform designed with privacy at its core. Leveraging state-of-the-art Large Language Models (LLMs), Prem provides a secure and flexible environment for self-hosting AI models or utilizing our privacy-focused cloud infrastructure.

## Getting Started

### Run the backend with docker-compose

```bash
docker-compose up --build -d
```

### Run the backend with Docker

```bash
docker run -d -v $(pwd)/models:/usr/src/app/models -e MODEL_WEIGHTS_DIR=./models -p 8002:8002 --name ai_box filippopedrazzini/the_ai_box:latest 
```

### Tasks

- [ ] Expose vicuna-7b-1.1-q4
- [ ] Expose whisper tiny. Save the weights in the dedicate folder.
- [ ] Expose stable diffusion latest model
- [ ] Expose emdeddings using llama or similar
- [ ] Expose embeddings using sentence-transformers/all-MiniLM-L6-v2
- [ ] Expose dolly-v2 or OA-30b-q4
- [ ] Pass `DEVICE` env variable
- [ ] Configure docker in order to handle m1 and gpu env
- [ ] Configure dependabot for dependencies
- [ ] Build a talk to your data use case using ai_box

### Fine Tune a model

- https://sebastianraschka.com/blog/2023/llm-finetuning-lora.html
- https://huggingface.co/bertin-project/bertin-alpaca-lora-7b
- https://twitter.com/realSharonZhou/status/1651989507615645696?s=20
- https://blog.replit.com/llm-training
- https://magazine.sebastianraschka.com/p/finetuning-large-language-models