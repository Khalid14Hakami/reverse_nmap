#!/bin/sh 
iptables -F
dst_ip =`ping -c1 c1 | sed -nE 's/^PING[^(]+\(([^)]+)\).*/\1/p'`
iptables -A OUTPUT -d $dst_ip -p tcp --tcp-flags SYN,ACK SYN,ACK -j DROP 
nc -l 2000