# syntax=docker/dockerfile:1

FROM python:3.8
RUN python -m pip install --upgrade pip
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/