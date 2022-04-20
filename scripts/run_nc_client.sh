#!/bin/sh 
echo "test" | nc -q 3 s1 1337
#echo "test" | nc -X connect -x 192.168.122.143:3128 s1 2000
exit 0