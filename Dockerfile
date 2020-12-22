# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

# install dependencies
RUN pip install --upgrade pip
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt

# copy project
COPY . .