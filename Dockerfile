# pull official base image
FROM python:3.7.10-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev alpine-sdk musl-dev libffi-dev

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
