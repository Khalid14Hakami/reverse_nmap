FROM ubuntu:latest
RUN apt update && apt install -y net-tools iputils-ping python curl netcat wget telnet systemctl && apt-get -y install vim nano  
VOLUME /etc /var

