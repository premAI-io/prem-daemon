# Prem ❤️

> Prem: A Privacy-Centric Open-Source AI Cloud Infrastructure Powered by Nostr. Leveraging state-of-the-art Large Language Models (LLMs), Prem provides a secure and flexible environment for self-hosting AI models quickly and efficiently.

<img width="1500" alt="CoverLogoIllustration2" src="https://github.com/premAI-io/prem-box/assets/29598954/d1e9a6a8-8e12-4ba9-865a-ac101a17e0a0">

## Prem Box

The `prem-box` is the primary repository used to build and serve the different AI services. Each docker image represents a service that can be run locally, in the Prem Cloud, or in your server infrastructure. The Prem architecture is structured around two main concepts:

- Controller: a simple FastAPI web server that uses the docker engine to run and manage the different images.
- Service: a single AI service that exposes certain endpoints based on a predefined scaffolding given by it's service type (or App).

The service can be run both on GPU and CPU hardware based on the model and the user hardware availability. Multiple options are available in order to handle this aspect.

## [Prem App](https://github.com/premAI-io/prem-app)

`prem-app` is the main interface for using `prem-box`. The frontend is integrated with both the controller and the workers to provide a pleasant experience for end-users.

Prem App can be run locally in two different ways:

- Desktop: You can download the .dmg and install the app on your Mac. [Download it here.](https://github.com/premAI-io/prem-app)
- Docker: Using docker-compose. Check the instructions in the #Installation section.

## [Prem Registry](https://github.com/premAI-io/prem-registry)

`prem-registry` contains all the manifests of all the services that `prem-box` exposes. `prem-box` fetches the metadata information from https://prem-registry.fly.dev/manifests/, which is a simple python webserver in order to expose the information of all the services in the repository. In order to submit a new service, please follow the instructions listed [here](https://github.com/premAI-io/prem-registry#packaging-a-service-for-prem-registry).

## [Prem Services](https://github.com/premAI-io/prem-services)

`prem-services` contains the services released by the core team. Each folder contains one or multiple services based on the model that has been exposed. We plan to create a cookiecutter template for an initial scaffolding.

## Prerequisites

We only support two hardware configurations. For what concerns the local installation, our docker images and containers are optimized for Apple Silicon users, while for the cloud users, we support NVIDIA GPUs.

## Installation

### LFG 🚀

```bash
docker-compose up -d
```
## Services

For a complete list of Apps and Services available in Prem Box, please check out our Prem Regisry at https://premai-io.github.io/prem-registry/.

### Running a single service on GPU

```bash
docker run -d -p 8000:8000 --gpus all --name prem_chat ghcr.io/premai-io/prem-chat-{model_id}-gpu:latest
```
### Running a single service on CPU

```bash
docker run -d -p 8000:8000 --platform linux/arm64 --name prem_chat ghcr.io/premai-io/prem-chat-{model_id}-m1:latest
```

## Product Roadmap

### Apps & Services

| App                                                                        | Deadline     |
| -------------------------------------------------------------------------- | ------------ |
| 😃 Prem Chat (missing [#6](https://github.com/premAI-io/ai-box/issues/6))  | 1st of June  |
| 📕 Prem Embeddings [#5](https://github.com/premAI-io/ai-box/issues/5)      | 1st of June  |
| 🏛️ Prem Store                                                              | 1st of June  |
| 🎨 Prem Michelangelo [#1](https://github.com/premAI-io/ai-box/issues/1)    | 10th of June |
| 💻 Prem Copilot [#2](https://github.com/premAI-io/ai-box/issues/2)         | 17th of June |
| 🎵 Prem Audio [#4](https://github.com/premAI-io/ai-box/issues/4)           | 24th of June |
| 📷 Prem Vision [#3](https://github.com/premAI-io/ai-box/issues/3)          | TBD          |
| 📖 Prem Summary [#24](https://github.com/premAI-io/ai-box/issues/24)       | TBD          |
| 🖼️ Prem Upscaler [#25](https://github.com/premAI-io/ai-box/issues/25)      | TBD          |
| 📹 Prem Video [#26](https://github.com/premAI-io/ai-box/issues/26)         | TBD          |

### Pipelines

Coming soon...

### Features

- [ ] Finetuning capabilities [#9](https://github.com/premAI-io/ai-box/issues/9)
- [ ] Data augmentation [#10](https://github.com/premAI-io/ai-box/issues/10)
- [ ] Prem Wallet [#11](https://github.com/premAI-io/ai-box/issues/11)
- [ ] Mobile App [#14](https://github.com/premAI-io/ai-box/issues/14)
- [ ] Plugins [#16](https://github.com/premAI-io/prem-box/issues/16)

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
