#!/bin/sh 
chmod 777 daemon/client_daemon.py scripts/* 
./scripts/iptables.sh
# ./daemon/client_daemon.py start 
