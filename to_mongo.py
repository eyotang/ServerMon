#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys, traceback, signal
import re, json, codecs

class PerfData(object):
    def __init__(self):
        dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.dirname = os.path.join(dirname, "result")
        self.metricsList = []

    def process(self):
        process_map = {
            "cpu_status": {"fields": ["user", "system"], "name": "cpuusage"},
            "disk_status": {"fields": ["rrqm", "wrqm"], "name": "diskusage"},
            "mem_status": {"fields": ["mem", "memswap"], "name": "memusage"},
            "network_status": {"fields": ["rxpck", "txpck", "rxkb", "txkb"], "name": "network"}
            }
        for filename in process_map.keys():
            path = os.path.join(self.dirname, filename)
            f = codecs.open(path, "r", "utf-8")
            process_map[filename]["fd"] = f

        for i in range(3):
            for _, content in process_map.items():
                f = content.get("fd")
                if not f:
                    continue
                line = f.readline()

        reached = False
        while True:
            metrics = {}
            for filename, content in process_map.items():
                f = content.get("fd")
                fields = content.get("fields")
                name = content.get("name")
                if not f:
                    continue
                line = f.readline().strip()
                if line:
                    record = {}
                    regex = re.compile("\s+")
                    values = regex.split(line)
                    for i in range(len(fields)):
                        record[fields[i]] = float(values[i])
                    metrics[name] = record
                else:
                    reached = True
            if reached:
                break
            else:
                self.metricsList.append(metrics)

        for _, content in process_map.items():
            f = content.get("fd")
            if f:
                f.close()

    def to_json(self):
        print("\"perfmetricslist\":%s" %(json.dumps(self.metricsList, indent=4)))


def onsignal_int(signum, frame) :
    print ("\nReceive SIGINT[Ctrl+C] to stop process by force !")
    sys.exit(-1)

def register_signal() :
    signal.signal(signal.SIGINT, onsignal_int)

def main() :
    register_signal()

    perf = PerfData()
    perf.process()
    perf.to_json()

if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception as e :
        traceback.print_exc(file = sys.stderr)
        sys.exit(2)
