#!/bin/sh

echo "Cleaning server 0"
ssh dtrustee-0.lb-ldd-diss.safer.isi.deterlab.net 'sudo pkill dissent'
echo "Cleaning server 1"
ssh dtrustee-1.lb-ldd-diss.safer.isi.deterlab.net 'sudo pkill dissent'
echo "Cleaning server 2"
ssh dtrustee-2.lb-ldd-diss.safer.isi.deterlab.net 'sudo pkill dissent'
echo "Cleaning client 0"
ssh dclient-0.lb-ldd-diss.safer.isi.deterlab.net 'sudo pkill dissent'
echo "Cleaning client 1"
ssh dclient-1.lb-ldd-diss.safer.isi.deterlab.net 'sudo pkill dissent'
echo "Cleaning client 2"
ssh dclient-2.lb-ldd-diss.safer.isi.deterlab.net 'sudo pkill dissent'
echo "Cleaning client 3"
ssh dclient-3.lb-ldd-diss.safer.isi.deterlab.net 'sudo pkill dissent'
echo "Cleaning client 4"
ssh dclient-4.lb-ldd-diss.safer.isi.deterlab.net 'sudo pkill dissent'

echo "Running on server 0"
ssh dtrustee-0.lb-ldd-diss.safer.isi.deterlab.net 'nohup ./dissent-simulation/dissent_exec dissent-simulation/server0.conf &'
echo "Running on server 1"
ssh dtrustee-1.lb-ldd-diss.safer.isi.deterlab.net 'nohup ./dissent-simulation/dissent_exec dissent-simulation/server1.conf &'
echo "Running on server 2"
ssh dtrustee-2.lb-ldd-diss.safer.isi.deterlab.net 'nohup ./dissent-simulation/dissent_exec dissent-simulation/server2.conf &'
echo "Running on client 0"
ssh dclient-0.lb-ldd-diss.safer.isi.deterlab.net 'nohup ./dissent-simulation/dissent_exec dissent-simulation/client0.conf &'
if [ -f "client1.conf" ]; then
    echo "Running on client 1"
    ssh dclient-1.lb-ldd-diss.safer.isi.deterlab.net 'nohup ./dissent-simulation/dissent_exec dissent-simulation/client1.conf &'
fi
if [ -f "client2.conf" ]; then
    echo "Running on client 2"
    ssh dclient-2.lb-ldd-diss.safer.isi.deterlab.net 'nohup ./dissent-simulation/dissent_exec dissent-simulation/client2.conf &'
fi
if [ -f "client3.conf" ]; then
    echo "Running on client 3"
    ssh dclient-3.lb-ldd-diss.safer.isi.deterlab.net 'nohup ./dissent-simulation/dissent_exec dissent-simulation/client3.conf &'
fi
if [ -f "client4.conf" ]; then
    echo "Running on client 4"
    ssh dclient-4.lb-ldd-diss.safer.isi.deterlab.net 'nohup ./dissent-simulation/dissent_exec dissent-simulation/client4.conf &'
fi