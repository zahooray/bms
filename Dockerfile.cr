FROM python:3.11-buster

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install pip-tools
