# Prem ❤️

> Prem: A Privacy-Centric Open-Source AI Cloud Infrastructure Powered by Nostr. Leveraging state-of-the-art Large Language Models (LLMs), Prem provides a secure and flexible environment for self-hosting AI models quickly and efficiently.

<img width="1500" alt="CoverOnlyLogoGradient" src="https://github.com/premAI-io/prem-box/assets/29598954/fd8fd553-b9c2-48b4-966d-cf933853d651">

## Prem Box

The `prem-box` is the primary repository used to build and serve the different AI services. Each docker image represents a service that can be run locally, in the Prem Cloud, or in your server infrastructure. The Prem architecture is structured around three main concepts:

- Controller: a simple FastAPI web server that uses the docker engine to run and manage the different images.
- Interface: defintion in terms of REST API that is used to constraint how a service should behave in terms of request and response in order to use it with a common interface.
- Service: a single AI service that exposes certain endpoints based on a predefined scaffolding given by it's interface.

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
docker run -d -p 8000:8000 --gpus all --name prem_chat ghcr.io/premai-io/hat-{model_id}-gpu:latest
```
### Running a single service on CPU

```bash
docker run -d -p 8000:8000 --platform linux/arm64 --name prem_chat ghcr.io/premai-io/chat-{model_id}-cpu:latest
```

## Product Roadmap

If you wanna know which services we support for each interface, please refer to Prem Registry https://premai-io.github.io/prem-registry/.

### Interfaces

- [x] 😃 Prem Chat
- [x] 📕 Prem Embeddings
- [x] 🏛️ Prem Store
- [ ] 🎨 Prem Michelangelo
- [ ] 💻 Prem Copilot
- [ ] 🎵 Prem Audio
- [ ] 📷 Prem Vision
- [ ] 📖 Prem Summary
- [ ] 🖼️ Prem Upscaler
- [ ] 📹 Prem Video

## Contributing

### Getting Started

```bash
# create a python virtual environment and activate it
virtualenv venv -p=3.10
source ./venv/bin/activate

# install the necessary dependencies
pip install -r requirements.txt

# configure pre-commit hooks
pre-commit install

# run the webserver
python main.py
```

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
- [replit](https://huggingface.co/replit)
- [stabilityai](https://huggingface.co/stabilityai)
- [whisper](https://github.com/openai/whisper)
- [bark](https://github.com/bark-simulator/bark)
- [salesforce](https://github.com/salesforce/CodeT5)
- [redis](https://redis.com/solutions/use-cases/vector-database/)
- [qdrant](https://github.com/qdrant/qdrant)
