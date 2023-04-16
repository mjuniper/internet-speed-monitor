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
OnCalendar=0/4:0:0
Unit=speedtest.service

[Install] 
WantedBy=timers.target
```

## systemctl commands:
systemctl stop speedtest.timer
systemctl disable speedtest.timer
systemctl enable speedtest.timer
systemctl start speedtest.timer
systemctl status speedtest.timer

systemctl list-timers  # view the status of the timers

journalctl  # view the full systemd logs
journalctl -u speedtest  # view the logs for a specific service
journalctl -f  # tail the logs
journalctl -f -u speedtest  # tail the logs for a specific service

# InfluxDB

## interacting with the influxdb database

```sh
$ influx
> use internetspeed
> select * from internet_speed
> select count(*) from internet_speed
```

http://localhost:8086/health
http://localhost:8086/debug/requests
http://localhost:8086/debug/vars
http://localhost:8086/query
http://localhost:8086/ping?verbose=true

## database size:

```sh
sudo du -sh /var/lib/influxdb/data/internetspeed
```

## config file

/etc/influxdb/influxdb.conf

```sh
influxd config
```

## Version

I am on InfluxDB v1.8 (`influxd version`) because it is 32 bit OS compatible

It might be good to upgrade to v2.X which would be a prette straightforward upgrade (see https://docs.influxdata.com/influxdb/v2.5/upgrade/v1-to-v2/automatic-upgrade/) EXCEPT that it does not support 32 bit OS.

Pretty sure there is no upgrade path for raspberry pi os 32 bit => 64 bit. So it would look something like:

1. Backup the influxdb database
1. Script the setup of everything (dependencies (speedtest-cli, python-dotenv), influxdb, grafana, systemd service and timer)
1. Make sure that script and everything else is pushed upstream into the github repo
1. Make an image of the sd card (as a backup in case this goes horribly wrong)
1. Use raspberry pi imager to write the new 64 bit os
1. Run the scripts to set everything up
1. Restore the db

# TODO

1. switch to the official influxdb python client library: https://docs.influxdata.com/influxdb/v2.0/api-guide/client-libraries/python/
1. setup automatic backups of influxdb onto another device or the cloud
1. use telegraf to collect the data and send it to influxdb - i think this would mean writing an input plugin... in Go