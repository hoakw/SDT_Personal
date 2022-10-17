FROM python:3.8-slim

RUN apt-get update && apt-get install -yq --no-install-recommends \
-y build-essential \
gcc \
curl 

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install --no-cache-dir -r ./requirements.txt

COPY . /app/
