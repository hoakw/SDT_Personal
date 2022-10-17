FROM golang:alpine

WORKDIR /app

COPY _certs /app/certs
COPY . /app/

ENTRYPOINT ["go", "run", ".", "--issuer", "https://dex.dex.svc:32000", "--listen", "http://0.0.0.0:5555", "--redirect-uri", "http://sdt.fastapi.com:32543/docs", "--issuer-root-ca", "/app/certs/ca.pem", "--debug"]