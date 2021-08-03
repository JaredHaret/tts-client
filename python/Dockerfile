FROM python:3.6-slim

ARG DEBIAN_FRONTEND=noninteractive

ADD ./python /tts_client

WORKDIR /tts_client

RUN ./setup.sh -y

RUN apt-get clean \
	&& rm -fr /var/lib/apt/lists/* \
	&& rm -fr /var/cache/apt/* 