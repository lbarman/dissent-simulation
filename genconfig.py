#!/usr/local/bin/python2

import sys
import os
from os.path import isfile, join

#constants
keyPath = "keys/private"
nClientMachines = 5
nServerMachines = 3

def writeClientConfig(machineID, localKeys, logPrefix):
    if len(localKeys) == 0:
        return

    file = open("client"+str(machineID)+".conf", "w") 
    file.write("[general]\n")
    file.write("remote_endpoints=\"tcp://11.1.0.1:51230\",\"tcp://11.1.0.2:51230\",\"tcp://11.1.0.3:51230\"\n")
    file.write("local_endpoints=\"tcp://11.0.1."+str(machineID+1)+":51229\"\n")
    file.write("local_nodes="+str(len(localKeys))+"\n\n")

    keys = ",".join(map(lambda elem : "\""+elem+"\"", localKeys))
    file.write("local_id="+keys+"\n")
    file.write("server_ids=\"QUTDkL8mYss2gBw-E2fx1GGAh2w=\",\"h8m9jFrEqu4bOcUBxYilGQMsYXE=\",\"9cLwIW23_RAtmxbzAsA6Rd6_3ME=\"\n")
    file.write("round_type=\"null/csdcnet\"\n\n")

    file.write("auth=true\n")
    file.write("path_to_private_keys=keys/private\n")
    file.write("path_to_public_keys=keys/public\n\n")


    file.write("console=false\n")
    file.write("exit_tunnel=false\n")
    file.write("log=\"dissent_logs/"+logPrefix+"_client"+str(machineID)+".log\"\n")
    file.write("multithreading=true\n\n")
    file.close() 


def writeServerConfig(machineID, localKey, logPrefix):
    file = open("server"+str(machineID)+".conf", "w") 
    file.write("[general]\n")
    file.write("remote_endpoints=\"tcp://11.1.0.1:51230\",\"tcp://11.1.0.2:51230\",\"tcp://11.1.0.3:51230\"\n")
    file.write("local_endpoints=\"tcp://11.1.0."+str(machineID+1)+":51230\"\n")
    file.write("local_nodes=1\n\n")

    file.write("local_id=\""+localKey+"\"\n")
    file.write("server_ids=\"QUTDkL8mYss2gBw-E2fx1GGAh2w=\",\"h8m9jFrEqu4bOcUBxYilGQMsYXE=\",\"9cLwIW23_RAtmxbzAsA6Rd6_3ME=\"\n")
    file.write("round_type=\"null/csdcnet\"\n\n")

    file.write("auth=true\n")
    file.write("path_to_private_keys=keys/private\n")
    file.write("path_to_public_keys=keys/public\n\n")


    file.write("console=false\n")
    file.write("exit_tunnel=false\n")
    file.write("log=\"dissent_logs/"+logPrefix+"_server"+str(machineID)+".log\"\n")
    file.write("multithreading=true\n\n")
    file.close() 


if len(sys.argv) != 3:
    print "1st argument must be NCLIENTS, 2nd must be LOGPREFIX"
    sys.exit(1);

nClients = int(sys.argv[1])
logPrefix = str(sys.argv[2])

print "Running master script for NCLIENTS =", nClients, ", LOGPREFIX = ", logPrefix

#read all identities
keysFiles = [f for f in os.listdir(keyPath) if isfile(join(keyPath, f))]

#Initially, all machines have no clients
keysOnClientMachines = {}
for i in range(0, nClientMachines):
    keysOnClientMachines[i] = []

#servers have a fixed assignement
keyOnServerMachines = {}
keyOnServerMachines[0] = "QUTDkL8mYss2gBw-E2fx1GGAh2w="
keyOnServerMachines[1] = "h8m9jFrEqu4bOcUBxYilGQMsYXE="
keyOnServerMachines[2] = "9cLwIW23_RAtmxbzAsA6Rd6_3ME="

#dispatch each client on a machine
currentMachine = 0
for i in range(0, nClients):
    keysOnClientMachines[currentMachine].append(keysFiles[i])
    currentMachine = (currentMachine + 1) % nClientMachines

#remove old config files
for i in range(0, nClientMachines):
    fname = "client"+str(i)+".conf"
    if os.path.isfile(fname):
        os.remove(fname)
for i in range(0, nServerMachines):
    fname = "server"+str(i)+".conf"
    if os.path.isfile(fname):
        os.remove(fname)

#create a config file for each machine
for i in range(0, nClientMachines):
    writeClientConfig(i, keysOnClientMachines[i], logPrefix)
for i in range(0, nServerMachines):
    writeServerConfig(i, keyOnServerMachines[i], logPrefix)