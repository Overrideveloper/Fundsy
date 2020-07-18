FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt
COPY ./alembic.ini /backend/alembic.ini

RUN pip install -r /backend/requirements.txt

COPY . /backend/

EXPOSE 8000