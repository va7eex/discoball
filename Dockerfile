FROM ubuntu:20.04

ENV DISCORD_TOKEN=""
ENV PRINTER_IP="127.0.0.1"
ENV LABELWIDTH=2
ENV LABELHEIGHT=1
ENV IMPERIALUNITS=TRUE
ENV TZ=Etc/UTC

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
	python3 \
	python3-pip \
        tzdata \
        iputils-ping

RUN pip3 install discord.py simple_zpl2 pillow python-dotenv profanity-filter

COPY discordbot.py ./
COPY labelmaker.py ./

ENTRYPOINT ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && ping -c 4 $PRINTER_IP > /dev/null 2>&1 && python3 -u discordbot.py || echo "Failed to locate printer"
