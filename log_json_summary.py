#!/usr/bin/python3

import sys
import json
from datetime import datetime
import math

currentPhase = "OFFLINE";
currentPhaseStartedAt = 0;
phasesDurations = {} # durations in seconds

sendReceiveDeltas = {}

def meanFn(array):
    if len(array) == 0:
        return 0;

    acc = 0.0
    for a in array:
        acc += a
    return acc / len(array)

# returns (mean, delta), where [mean - delta; mean + delta] is the 95% confidence interval for the mean
def meanAndConfDelta(data):
    if len(data) == 0:
        return (0, 0)
    mean = meanFn(data)

    deviations = [];
    for val in data:
        diff = mean - val
        deviations.append(diff * diff)

    variance = meanFn(deviations)
    dev = math.sqrt(variance)
    sigma = dev / math.sqrt(len(data))
    z_value_95 = 1.96
    delta = sigma * z_value_95

    mean_r = round(mean * 10090) / 10000
    delta_r = round(delta * 10090) / 10000

    return (mean_r, delta_r)

def pad(s, i):
    if len(s) < i:
        return (' ' * (i - len(s)) ) + s;
    return s;

def processFile(inFile, outFile):
    global currentPhase, currentPhaseStartedAt, phasesDurations, sendReceiveDeltas

    toPrint = []

    i=0

    with open(inFile) as file:
        rawData = file.read()
        lines = rawData.strip().split("\n")
        blob = '[' + ','.join(lines) + ']';
        data = json.loads(blob);

        # computes phases durations
        for line in data:
            if line['_type'] == 'phase':
                oldPhase = line['stateEnded'];
                if oldPhase != currentPhase:
                    print("Logs said oldphase is", oldPhase, "but it is", currentPhase);
                    currentPhase = oldPhase;

                oldPhaseDuration = line['time'] - currentPhaseStartedAt;

                if not oldPhase in phasesDurations:
                    phasesDurations[oldPhase] = []

                phasesDurations[oldPhase].append(oldPhaseDuration);

                currentPhase = line['stateStarted'];
                currentPhaseStartedAt = line['time'];

        print("Phases durations: [s]")
        for phase in phasesDurations:
            mean, delta = meanAndConfDelta(phasesDurations[phase])
            print(pad(phase, 30), ": Mean ", mean, " confidence ", delta);
            toPrint.append({'_type': phase, 'mean': mean, 'delta': delta})

        sendReceiveDeltasArray = [];

        for line in data:
            if line['_type'] == 'send':
                dataSent = line['data_id'];
                sendReceiveDeltas[dataSent] = "INF";
                for line2 in data:
                    if line2['_type'] == 'receive' and line2['data_id'] == dataSent:
                        sendReceiveDeltas[dataSent] = line2['time'] - line['time']

                if sendReceiveDeltas[dataSent] != "INF":
                    sendReceiveDeltasArray.append(sendReceiveDeltas[dataSent])

        # merge as an array
        print("")
        print("Send-receive latency: [s]")
        mean, delta = meanAndConfDelta(sendReceiveDeltasArray)
        print("mean: ", mean);
        print("delta: ", delta);

        toPrint.append({'_type': 'latencies', 'mean': mean, 'delta': delta})

    with open(outFile, "w") as file:
        for line in toPrint:
            file.write(json.dumps(line, sort_keys=True)+"\n")


if len(sys.argv) < 2:
    print("Argument 1 must be the input file")
    sys.exit(1)

if len(sys.argv) < 3:
    print("Argument 2 must be the output file")
    sys.exit(1)

a = str(sys.argv[1])
b = str(sys.argv[2])
processFile(a, b)