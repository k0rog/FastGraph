FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /fast_graph
COPY requirements.txt /fast_graph/requirements.txt
RUN pip install -r requirements.txt
COPY ./app /fast_graph/app
COPY ./main.py /fast_graph/main.py
COPY ./tests /fast_graph/tests
COPY ./pytest.ini /fast_graph/pytest.ini
ARG DEBIAN_FRONTEND=noninteractive

RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*
RUN apt update
RUN apt install postgresql postgresql-contrib -f -y
RUN adduser testuser --gecos '' --disabled-login
USER testuser