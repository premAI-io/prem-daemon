FROM python:3.10-slim-bullseye

WORKDIR /usr/src/app/

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt --upgrade pip

COPY . .

CMD gunicorn --bind 0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornWorker main:app
