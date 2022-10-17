FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -yq --no-install-recommends \
-y build-essential \
gcc \
curl 

RUN pip install --no-cache-dir kserve \
typing \
pandas \
numpy \
sklearn \
mlflow 

ENV APP_HOME /app
WORKDIR $APP_HOME

# Install production dependencies.
COPY . $APP_HOME/

CMD ["python3", "main.py"]