FROM python:3.10-slim-bullseye
WORKDIR /usr/src/app/

RUN apt update -qq && apt install -yqq --no-install-recommends \
    gcc curl \
    build-essential \
    libc6-dev \
    python3-dev \
    && curl -fsSL https://get.docker.com | sed 's/if is_wsl/if false/' | sh \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD python main.py
