#!/bin/bash

export GO111MODULE=on
go mod vendor

go build -o `pwd`/output/status_controller -gcflags all=-trimpath=`pwd` -asmflags all=-trimpath=`pwd` -mod=mod `pwd`/src/main

# docker build and push
#docker build -t hoakw/status_test:v1.0 ./
#docker push hoakw/status_test:v1.0 

