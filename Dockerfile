FROM python:3.11

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requrements.txt

ENV TZ Europe/Moscow



CMD python bot.py