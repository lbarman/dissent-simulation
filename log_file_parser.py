#!/usr/bin/python3

import sys
import json
from datetime import datetime

starting_time = None

events = []

def time_parse0(str_time):
  return datetime.strptime(str_time, "%Y-%m-%dT%H:%M:%S.%f")

def time_parse(str_time):
  ctime = datetime.strptime(str_time, "%Y-%m-%dT%H:%M:%S.%f")
  td = ctime - starting_time
  return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1000000.0) / 1000000.0

def processFile(inFile, outFile):
    global starting_time, events

    i=0

    with open(inFile) as file:
        rawData = file.read()
        lines = rawData.split("\n")

        time = time_parse0(lines[0].split(" ")[0])
        starting_time = time

        for line in lines:

            line2 = ""
            if "Debug - Got message" in line:
                o = {}
                o['_type'] = 'receive'
                o['id'] = i
                time = time_parse(line.split(" ")[0])
                o['time'] = time
                data = line.split(" ")[6].replace("\"", "")
                o['data_id'] = data

                events.append(o)

            if "Handling request for  QUrl" in line and "/session/send" in line:
                o = {}
                o['_type'] = 'send'
                o['id'] = i
                time = time_parse(line.split(" ")[0])
                o['time'] = time
                url = line.split(" ")[9].replace("\"", "")
                o['url'] = url
                o['data_id'] = ''
                if '?' in url:
                    o['data_id'] = url[url.find("?data=")+6:]
                i += 1

                events.append(o)

            if "Phase: " in line:
                line2 = line[line.find("Phase: ")+"Phase: ".__len__():]
                time = time_parse(line.split(" ")[0])

                phaseNo = line2[0:line2.find("\"")]
                if "ending:" in line2 and "starting:" in line2:
                    parts = line2.split(" ");
                    stateEnded = parts[2].replace("\"", "")
                    stateStarted = parts[4].replace("\"", "")
                    o = {}
                    o['_type'] = 'phase'
                    o['id'] = i
                    o['time'] = time
                    o['phase'] = phaseNo
                    o['stateEnded'] = stateEnded
                    o['stateStarted'] = stateStarted

                    events.append(o)
                    i+=1

    with open(outFile, "w") as file:
        for line in events:
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