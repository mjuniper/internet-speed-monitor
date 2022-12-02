# internet-speed-monitor

Tests internet speed at intervals, and pushes the data into an influxdb database

loosely based on https://pimylifeup.com/raspberry-pi-internet-speed-monitor/

# Instructions

## Per the article above, you need to:
- install the speedtest-cli
- install influxdb and setup your database
- use cron, systemd, or _something_ to run the speedtest.py script at some interval
- install grafana and point it at your database (this step is optional, the script will work regardless, but sorta the whole point)

## Prerequisites not listed in the article above
- pip install python-dotenv
- create a .env file in the root of the project that looks like the following:

```
HOST="localhost"
PORT="8086"
USERNAME="speedmonitor"
PASSWORD="<your password>"
DATABASE="internetspeed"
TABLE="internet_speed"
```

## Note

I found that my raspberry pi gets ~70 Mbps down on wifi but ~350 Mbps down on ethernet. My MBA sitting right next to it gets ~350 Mbps on the same wifi network. Not sure why the pi's wifi is so slow.

## Scheduling the script:

```
# /etc/systemd/system/speedtest.service
[Unit]
Description=Run speedtest.sh

[Service]
User=pi
ExecStart=/bin/sh  /home/pi/Dev/internet-speed-monitor/speedtest.sh
```

```
# /etc/systemd/system/speedtest.timer
[Unit]
Description=Speedtest job timer

[Timer]
OnBootSec=1min
OnCalendar=0/3:0:0
Unit=speedtest.service

[Install] 
WantedBy=timers.target
```

## systemctl commands:
systemctl start speedtest
systemctl stop speedtest
systemctl status speedtest

systemctl list-timers  # view the status of the timers

journalctl  # view the full systemd logs
journalctl -u speedtest  # view the logs for a specific service
journalctl -f  # tail the logs
journalctl -f -u speedtest  # tail the logs for a specific service

# interacting with the influxdb database

```sh
$ influx
> use internetspeed
> select * from internet_speed
> select count(*) from internet_speed
```