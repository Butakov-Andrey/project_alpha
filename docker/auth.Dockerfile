FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY apps/auth/requirements.txt /code/requirements.txt

RUN pip install --upgrade pip \
                --no-cache-dir -r requirements.txt

COPY ./apps/auth /code/
