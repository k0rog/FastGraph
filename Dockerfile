FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /fast_graph
COPY requirements.txt /fast_graph/requirements.txt
RUN pip install -r requirements.txt
COPY ./app /fast_graph/app
COPY ./main.py /fast_graph/main.py