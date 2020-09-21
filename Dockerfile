FROM ubuntu:20.04

ENV DISCORD_TOKEN=""
ENV PRINTER_IP="127.0.0.1"

RUN apt update && apt install -y \
	python3 \
	python3-pip

RUN pip3 install discord.py simple_zpl2 pillow

COPY discordbot.py ./
COPY labelmaker.py ./
