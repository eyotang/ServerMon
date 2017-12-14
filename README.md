# ServerMon
Server performance monitor by python

## Usage

Start tool to collect server performance KPI.
```
./start_collect.py
```

Put the traffic on this server.
Collecter will exit automatically, when the traffic stopped, if the server is used purely for traffic test.
Otherwise, you can stop it by Ctl+C.

Run abstractor to abstract KPI data.
```
./abstract_data.py
```
