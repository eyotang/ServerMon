#!/bin/bash

INTERVAL_TIME=1

sar -n DEV ${INTERVAL_TIME} >>res/NetWork &
iostat -x -d -k ${INTERVAL_TIME} >>res/Disk &
sar -r ${INTERVAL_TIME} >>res/Memory &
sar -q ${INTERVAL_TIME} >>res/System_load_average &
sar -u ${INTERVAL_TIME} >>res/CPU &
sar -b ${INTERVAL_TIME} >>res/TPS &
