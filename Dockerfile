FROM python:3.9.0

WORKDIR /usr/app

COPY ./ /usr/app

RUN pip install -r requirements.txt