FROM python:3.7.2-alpine3.8
ENV PYTHONUNBUFFERED 1

RUN apk --no-cache add build-base
RUN apk add --no-cache bash
RUN apk --no-cache add postgresql-dev 
RUN apk add openrc --no-cache
RUN apk add --no-cache tzdata

RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install pipenv

RUN chmod 755 /code/record.sh /code/entry.sh /code/consolidate.sh

ENV TZ America/Chicago