#!/usr/local/bin/bash

rm automate.log

maxRetriesForOneBatch=3
oneBatchSleepTime=180

# $1 is the filename, e.g. exp1_0_send.log, $2 is the retry number
function testIfReportingOK {
    fileName="$1"
    retries="$2"
    
    # extracts the last sent id
    #lastReportingNumber=$(cat "$fileName" | tail -n 1 | cut -d':' -f 4 | cut -d' ' -f 2)
    
    # extracts the last received id
    lastReportingNumber=$(cat "$fileName" | grep "Got message" | tail -n 1 | cut -d':' -f 4 | cut -d' ' -f 2 | cut -d'"' -f 2 | sed 's/data//g')

    if [ -z "$lastReportingNumber" ]; then
        
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

for roundType in "null/csdcnet" "verif"
do
    for repeat in 0 1 2 3 4 5 6 7 8 9
    do
        for nclients in 1 10 20 30 40 50 60 70 80 90 100
        do
            logPrefix=$(echo "exp${nclients}_${repeat}_${roundType}" | tr / -)
            echo "Starting for $roundType, $nclients, repeat $repeat (logPrefix ${logPrefix})..."
            python2 genconfig.py $nclients "${logPrefix}" "$roundType"
            ./run_all.sh

            sleep "$oneBatchSleepTime"

            echo -n "experiment running for $roundType, $nclients, repeat $repeat... (logPrefix ${logPrefix})"
            testIfReportingOK "${logPrefix}_client0.log" 10

            ./killall.sh
            rm *.conf
        done
    done
done