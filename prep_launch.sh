#!/bin/sh 
chmod 777 client_daemon.py scripts/* iptables.sh
./iptables.sh
./client_daemon.py start 
