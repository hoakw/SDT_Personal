FROM ubuntu:16.04

ENV OPERATOR=/usr/local/bin/status_controller 

RUN apt-get update && apt-get -y install iputils-ping

COPY output/status_controller ${OPERATOR}

#COPY output/bin /usr/local/bin
#RUN  /usr/local/bin/user_setup


#USER status-controller
ENTRYPOINT ["/usr/local/bin/status_controller"]

#USER ${USER_UID}

#ENTRYPOINT ["/user/local/bin/status_controller"]
