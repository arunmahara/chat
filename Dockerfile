# syntax=docker/dockerfile:1
FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir && \
    python3 -m pip install -U channels["daphne"]

RUN rm -f requirements.txt

WORKDIR /chat
COPY manage.py .
COPY chat/ ./chat/
