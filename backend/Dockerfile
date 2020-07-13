FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./alembic.ini /app/alembic.ini

RUN pip install -r /app/requirements.txt

COPY . /app/

EXPOSE 8000