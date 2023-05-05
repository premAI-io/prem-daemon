FROM python:3.10-slim-bullseye

ARG MODEL_ID

RUN apt update && apt install -y libopenblas-dev ninja-build build-essential
RUN python -m pip install --upgrade pip pytest cmake scikit-build setuptools

WORKDIR /usr/src/app/

COPY /requirements/ ./requirements/

RUN pip install --no-cache-dir -r ./requirements/chat/llamacpp.txt --upgrade pip

COPY . .

ENV MODEL_ID=$MODEL_ID

CMD python main.py
