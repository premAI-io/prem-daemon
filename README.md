# Prem ❤️

> Prem: A Privacy-Centric Open-Source AI Cloud Infrastructure Powered by Nostr. A cutting-edge, open-source AI platform designed with privacy at its core. Leveraging state-of-the-art Large Language Models (LLMs), Prem provides a secure and flexible environment for self-hosting AI models or utilizing our privacy-focused cloud infrastructure.

## Prem Box

The `prem-box` is the primary repository used to build and serve the different AI services. Each docker image represents a service that can be run locally, in the Prem Cloud, or in your server infrastructure. The repository is structured around two main concepts:

- Controller: a simplified FastAPI web server that uses the docker engine to run the different images.
- Worker: a single AI service exposed with a FastAPI web server using similar endpoints to those of OpenAI based on the task it is implemented to perform (e.g., `chat-completions`, `embeddings`, `images-generation`).
The worker can be run on both GPU and CPU hardware based on the model and the user hardware availability. Multiple options are available for handling this aspect.

## [Prem App](https://github.com/premAI-io/prem-app)

`prem-app` is the main interface for using `prem-box`. The frontend is integrated with both the controller and the workers to provide a pleasant experience for end-users.

Prem App can be run locally in two different ways:

- Desktop: You can download the .dmg and install the app on your Mac. [Download it here.](https://google.com)
- Docker: Using docker-compose. Check the instructions in the #Installation section.

## Prerequisites

We only support two hardware configurations. For what concerns the local installation, our docker images and containers are optimized for Apple Silicon users, while for the cloud users, we support NVIDIA GPUs.

## Installation

### LFG 🚀

```bash
docker-compose up -d
```
## Services

### Prem Chat & Embeddings

| Model                                     | Model ID                    | Memory              | Device  | Chat | Embeddings |
| ----------------------------------------- | --------------------------- | ------------------- | ------- | ---- | ---------- |
| Vicuna 7B 4-bit                           | vicuna-7b-q4                | 16gb                | CPU     | Yes  | Yes        |
| GPT4All 4-bit                             | gpt4all-lora-q4             | 16gb                | CPU     | Yes  | Yes        |
| Dolly v2 12B                              |                             | 24gb                | GPU     | Yes  | No         |
| OpenAssistant Llama 30B XOR               |                             | 48gb                | GPU     | Yes  | No         |
| All-MiniLM-L6-v2                          |                             | 16gb                | GPU     | No   | Yes        |

### Running a single service on GPU

```bash
docker run -d -p 8000:8000 --gpus all --name prem_chat ghcr.io/premai-io/prem-chat-{model_id}-gpu:latest
```
### Running a single service on CPU

```bash
docker run -d -p 8000:8000 --platform linux/arm64 --name prem_chat ghcr.io/premai-io/prem-chat-{model_id}-m1:latest
```

## Product Roadmap

### Services

| App                                                                        | Deadline     |
| -------------------------------------------------------------------------- | ------------ |
| 😃 Prem Chat (missing [#6](https://github.com/premAI-io/ai-box/issues/6))  | 1st of June  |
| 📕 Prem Embeddings ([#5](https://github.com/premAI-io/ai-box/issues/5))    | 1st of June  |
| 🏛️ Prem Store                                                              | 1st of June  |
| 🎨 Prem Michelangelo [#1](https://github.com/premAI-io/ai-box/issues/1)    | 10th of June |
| 💻 Prem Copilot [#2](https://github.com/premAI-io/ai-box/issues/2)         | 17th of June |
| 🎵 Prem Audio [#4](https://github.com/premAI-io/ai-box/issues/4)           | 24th of June |
| 📷 Prem Vision [#3](https://github.com/premAI-io/ai-box/issues/3)          | TBD          |

### Pipelines

Coming soon...

### Features

- [ ] Finetuning capabilities ([#9])
- [ ] Data augmentation ([#10])
- [ ] Prem Wallet ([#11])
- [ ] Mobile App ([#14])

## Contributing

Depending on which component you are contributing to, you will have different hardware requirements. In order to run certain models you need at least 48gb of VRAM, which makes it difficult for a common developer to contribute in terms of these models. On the other hand, a lot of components can be run easily on consumer hardware. In that case, our suggestion is to write test cases accordingly and end-to-end test the app with the deployment command.

## Product Documentation

### FAQ

**How to install Docker Desktop?**

**How to free some space?**

**Which Hardware do I need to run Prem?**

**Trobleshooting**

## Acknowledgments

Thank You ❤️

- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [gpt4all](https://github.com/nomic-ai/gpt4all)
- [dolly-v2-12b](https://huggingface.co/databricks/dolly-v2-12b)
- [Open-Assistant](https://github.com/LAION-AI/Open-Assistant)
- [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [vicuna-7b](https://github.com/lm-sys/FastChat)
