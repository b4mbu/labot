FROM python:3.9-slim-bullseye

COPY main.py .
COPY src src
COPY requirements.txt .
COPY config config
COPY .env .

RUN pip3 install -r requirements.txt
