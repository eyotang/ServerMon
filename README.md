# ServerMon
Server performance monitor by python

## Usage
required >=Python3.4

Start tool to collect server performance KPI.
```
./start_collect.py
```

Put the traffic on this server.
Collecter will exit automatically, when the traffic stopped, if the server is used purely for traffic test.
Otherwise, you can stop it by Ctl+C.

Collected performance data will be uploaded to report server.
