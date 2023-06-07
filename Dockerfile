FROM python:3.10-slim-bullseye

WORKDIR /usr/src/app/

RUN apt-get update && apt-get install -y gcc

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt --upgrade pip

COPY . .

CMD python main.py
