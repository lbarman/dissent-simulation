#!/bin/sh

rm automate.log

for repeat in {0..10}
do
    for nclients in 1 10 20 30 40 50 60 70 80 90 100
    do
        echo "Running for $nclients, repeat $repeat..." | tee automate.log
        python2 genconfig.py $nclients "exp${nclients}_${repeat}"
        ./run_all.sh

        sleep 180
        ./killall.sh
        rm *.conf
    done
done