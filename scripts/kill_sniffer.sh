#!/bin/bash  

# interrupt the sniffer.  get its PID:  
pid=$(ps -e | pgrep tcpdump)  
echo $pid  

#interrupt it:  
sleep 5
kill -2 $pid