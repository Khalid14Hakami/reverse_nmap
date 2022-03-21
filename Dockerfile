FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y iptables tcpdump squid net-tools iputils-ping python python3-pip curl netcat wget telnet systemctl git && apt-get -y install vim nano  
VOLUME /etc /var /home /root /usr

