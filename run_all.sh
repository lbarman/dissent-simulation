#!/bin/sh

echo "Cleaning server 0"
ssh dtrustee-0.lb-ldd-diss.safer.isi.deterlab.net 'sudo pkill dissent'
echo "Cleaning server 1"
ssh dtrustee-1.lb-ldd-diss.safer.isi.deterlab.net 'sudo pkill dissent'
echo "Cleaning server 2"
ssh dtrustee-2.lb-ldd-diss.safer.isi.deterlab.net 'sudo pkill dissent'
echo "Cleaning client 0"
ssh dclient-0.lb-ldd-diss.safer.isi.deterlab.net 'sudo pkill dissent'
ssh dclient-0.lb-ldd-diss.safer.isi.deterlab.net 'sudo pkill send_data'
echo "Cleaning client 1"
ssh dclient-1.lb-ldd-diss.safer.isi.deterlab.net 'sudo pkill dissent'
echo "Cleaning client 2"
ssh dclient-2.lb-ldd-diss.safer.isi.deterlab.net 'sudo pkill dissent'
echo "Cleaning client 3"
ssh dclient-3.lb-ldd-diss.safer.isi.deterlab.net 'sudo pkill dissent'
echo "Cleaning client 4"
ssh dclient-4.lb-ldd-diss.safer.isi.deterlab.net 'sudo pkill dissent'

echo "Running on server 0"
ssh dtrustee-0.lb-ldd-diss.safer.isi.deterlab.net 'cd dissent-simulation && ./run.sh server0.conf'
echo "Running on server 1"
ssh dtrustee-1.lb-ldd-diss.safer.isi.deterlab.net 'cd dissent-simulation && ./run.sh server1.conf'
echo "Running on server 2"
ssh dtrustee-2.lb-ldd-diss.safer.isi.deterlab.net 'cd dissent-simulation && ./run.sh server2.conf'
echo "Running on client 0"
ssh dclient-0.lb-ldd-diss.safer.isi.deterlab.net 'cd dissent-simulation && ./run.sh client0.conf && ./start_send_data.sh'
if [ -f "client1.conf" ]; then
    echo "Running on client 1"
    ssh dclient-1.lb-ldd-diss.safer.isi.deterlab.net 'cd dissent-simulation && ./run.sh client1.conf'
fi
if [ -f "client2.conf" ]; then
    echo "Running on client 2"
    ssh dclient-2.lb-ldd-diss.safer.isi.deterlab.net 'cd dissent-simulation && ./run.sh client2.conf'
fi
if [ -f "client3.conf" ]; then
    echo "Running on client 3"
    ssh dclient-3.lb-ldd-diss.safer.isi.deterlab.net 'cd dissent-simulation && ./run.sh client3.conf'
fi
if [ -f "client4.conf" ]; then
    echo "Running on client 4"
    ssh dclient-4.lb-ldd-diss.safer.isi.deterlab.net 'cd dissent-simulation && ./run.sh client4.conf'
fi