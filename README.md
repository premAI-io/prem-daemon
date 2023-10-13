# 🏃Prem Daemon

[![image:premd](https://img.shields.io/github/actions/workflow/status/premAI-io/prem-daemon/on-tag.yml?logo=docker&label=premd
)](https://github.com/premAI-io/prem-daemon/pkgs/container/premd)

## Prem Architecture

Prem ecosystem is based on multiple repositories and components that are developed and maintained by Prem team.

- [Prem Services](https://github.com/premAI-io/prem-services): the repository contains the source code of the services that are developed and mantained by Prem team. Each service is a Docker image exposing certain HTTP APIs based on a predefined interface. Currently, Prem supports the following interfaces:
    - Chat
    - Embeddings
    - Vector Store
    - Diffuser
    - Text to Audio
    - Audio to Text
    - Coder
- [Prem Registry](https://github.com/premAI-io/prem-registry): the repository contains all the services that are available in the Prem ecosystem and can be used by the Prem Daemon.
    - `main`: contains the latest stable version of the services.
    - `dev`: contains the latest version of the services that are under development.
- [Prem Daemon](https://github.com/premAI-io/prem-daemon): the repository contains the source code of the Prem Daemon which is the component responsible to launch the different services.
- [Prem App](https://github.com/premAI-io/prem-app): the repository contains the source code of the Prem App. Prem App represents the user interface used to interact with the Prem Daemon and the Prem Services.

The information flow works as following:

Prem App sends HTTP requests to Prem Daemon. Prem Daemon is responsible to launch the requested service and to return the response to Prem App. Prem Daemon using Docker SDK starts the requested service as a Docker container. Based on the interface exposed by the service, Prem App can directly interact with the service or it can use Prem Daemon as a proxy.

## Contributing to Prem Daemon

### Running the Daemon locally

```bash
git clone https://github.com/premAI-io/prem-daemon.git
cd ./prem-daemon

# create a python virtual environment and activate it
virtualenv venv -p=3.10
source ./venv/bin/activate

# install the necessary dependencies
pip install -r requirements.txt

# configure pre-commit hooks
pre-commit install

# run the webserver
cp .env.example .env
python main.py
```

### Running the daemon locally with Docker
#### From source
```bash
docker build -t premd .
docker run -it -v /var/run/docker.sock:/var/run/docker.sock -p 54321:8000 --name premd -e PREM_REGISTRY_URL=https://raw.githubusercontent.com/premAI-io/prem-registry/main/manifests.json --rm premd
```

#### From DockerHub
```bash
docker run -d -v /var/run/docker.sock:/var/run/docker.sock -p 54321:8000 --name premd -e PREM_REGISTRY_URL=https://raw.githubusercontent.com/premAI-io/prem-registry/main/manifests.json --rm ghcr.io/premai-io/premd:v0.0.28@sha256:2369e38cbcece1f354917cd2c8290d1f8859264dc081ae036cee419bf858c4ab
```

### Mock Registry

[![image:mock](https://img.shields.io/github/actions/workflow/status/premAI-io/prem-daemon/on-main.yml?logo=docker&label=mock%20images
)](https://github.com/orgs/premAI-io/packages?tab=packages&q=mock)

In order to use the mock registry, you can specify the `REGISTRY_URL` environment variable as following:

```bash
PREM_REGISTRY_URL=https://raw.githubusercontent.com/premAI-io/prem-daemon/main/resources/mocks/manifests.json
```

> The mock registry is not fully tested. Few interfaces could be broken.

### Dev Registry

In order to use the dev registry, you can specify the `REGISTRY_URL` environment variable as following:

```bash
PREM_REGISTRY_URL=https://raw.githubusercontent.com/premAI-io/prem-registry/dev/manifests.json
```

### Custom Registry

Prem is fully open source, you can specify whatever url you prefer that contains a json file in the same format as Prem Registry and the services will be handled accordingly.

You just need to run `premd` with `PREM_REGISTRY_URL` env variable.

### Running the test cases

```bash
pytest
```
