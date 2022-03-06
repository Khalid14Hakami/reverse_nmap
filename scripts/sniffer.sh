#!/bin/bash  

#start a process in the background (it happens to be a TCP HTTP sniffer on  the loopback interface, for my apache server):   

tcpdump -U -w /root/reverse_nmap/test_capture.pcap host c1 or host s1& 
sleep 5

# interrupt the sniffer.  get its PID:  
pid=$(ps -e | pgrep tcpdump)  
echo $pid  

#interrupt it:  
sleep 180s
kill -2 $pid