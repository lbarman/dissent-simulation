#!/bin/bash

sleep 10

i=1
while true
do
    data="data$i"
    echo -en "Sending $data\t\t"
    curl -s --data "$data" http://localhost:8080/session/send\?data=$1 1>/dev/null 2>&1
    curl -s http://localhost:8080/session/messages\?offset\=0\&count\=999999999999
    echo ""
    sleep 1
    i=$((i+1))
done
