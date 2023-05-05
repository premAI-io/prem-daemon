FROM python:3.10-slim-bullseye

WORKDIR /usr/src/app/

COPY /requirements/ ./requirements/

RUN pip install --no-cache-dir -r ./requirements/controller.txt --upgrade pip

COPY . .

CMD python main.py
