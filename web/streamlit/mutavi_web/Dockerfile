FROM python:3.8-slim-buster AS builder

#Image description
LABEL maintainer="Mobiis ML team"
LABEL title="mutavi_web"
LABEL version="0.1"
LABEL description="streamlit app for mutavi web"

RUN apt-get update && apt-get install -yq --no-install-recommends \
-y build-essential \
gcc \
curl 

# Install python packages
COPY requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt

FROM python:3.8-slim-buster
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/local/bin/streamlit /usr/local/bin/streamlit
ENV PATH $PATH:/usr/local/bin/streamlit

# Set working directory
ENV APP_HOME=/app
COPY . $APP_HOME/
WORKDIR $APP_HOME

ENTRYPOINT [ "streamlit", "run" ]
CMD ["muta.py"]