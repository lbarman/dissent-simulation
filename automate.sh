#!/usr/local/bin/bash

rm automate.log

maxRetriesForOneBatch=3
oneBatchSleepTime=180

# $1 is the filename, e.g. exp1_0_send.log, $2 is the retry number
function testIfReportingOK {
    fileName="$1"
    retries="$2"
    lastReportingNumber=$(cat "$fileName" | tail -n 1 | cut -d':' -f 4 | cut -d' ' -f 2)
    if [ "$lastReportingNumber" -eq 0 ]; then
        
        if [ $retries -lt $maxRetriesForOneBatch ]; then

            echo -n "Wait($retries),"
            sleep "$oneBatchSleepTime"
            testIfReportingOK "$fileName" $(($retries+1))

        else 

            echo "Failed."

        fi

    else
        echo "Success".
    fi
}

for repeat in 0 1 #2 3 4 5 6 7 8 9
do
    for nclients in 1 10 #20 30 40 50 60 70 80 90 100
    do
        echo "Starting for $nclients, repeat $repeat..." | tee automate.log
        python2 genconfig.py $nclients "exp${nclients}_${repeat}"
        ./run_all.sh

        sleep "$oneBatchSleepTime"

        echo -n "experiment running for $nclients, repeat $repeat... "
        testIfReportingOK "exp${nclients}_${repeat}_send.log" 1

        ./killall.sh
        rm *.conf
    done
done
