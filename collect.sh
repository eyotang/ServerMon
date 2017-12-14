#!/bin/bash

sar -n DEV 10 >>res/NetWork &
iostat -x -d -k 10 >>res/Disk &
sar -r 10 >>res/Memory &
sar -q 10 >>res/System_load_average &
sar -u 10 >>res/CPU &
sar -b 10 >>res/TPS &
