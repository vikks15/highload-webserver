FROM ubuntu:16.04

MAINTAINER vikks15

RUN apt-get update &&\
        apt-get install -y python3

EXPOSE 80

CMD python3 main.py