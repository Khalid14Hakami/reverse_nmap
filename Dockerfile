FROM ubuntu:latest
RUN apt update && apt install -y iptables tcpdump squid net-tools iputils-ping python curl netcat wget telnet systemctl git && apt-get -y install vim nano  
VOLUME /etc /var /home /root

