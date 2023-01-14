FROM python:3.8-buster

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY config/requirements/dev.txt /code/
RUN pip install --upgrade pip
RUN pip install -r /code/dev.txt
