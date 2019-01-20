FROM python:3.7.2-alpine3.8
ENV PYTHONUNBUFFERED 1
ENV PULSE_HOST_TYPE dev

RUN apk add --no-cache bash

RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install pipenv