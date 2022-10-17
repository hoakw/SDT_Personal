FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -yq --no-install-recommends \
-y build-essential \
gcc \
curl 

RUN pip install requests --no-cache-dir

ENV APP_HOME=/APP_HOME

COPY . $APP_HOME
WORKDIR $APP_HOME

CMD ["python3", "test.py"]
