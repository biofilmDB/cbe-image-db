FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apk add --update curl gcc g++\
    && rm -rf /var/cache/apk/*

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
