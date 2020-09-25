FROM ubuntu:20.04

ENV DISCORD_TOKEN=""
ENV PRINTER_IP="127.0.0.1"
ENV TZ=Etc/UTC

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
	python3 \
	python3-pip \
        tzdata

RUN pip3 install discord.py simple_zpl2 pillow python-dotenv

COPY discordbot.py ./
COPY labelmaker.py ./

ENTRYPOINT ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && bash
