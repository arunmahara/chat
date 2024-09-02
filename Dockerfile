# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /<work-dir>
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#COPY <chat> .env* Dockerfile manage.py /<work-dir>/