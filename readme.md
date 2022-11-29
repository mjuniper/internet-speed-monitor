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

# TODO:
  - use systemctl to run the job at intervals instead of crontab
  - alternatively i could refactor the script to do the speedtest in a loop and just use systemd (or cron or whatever) to start the script on boot - not sure which is better...

===

# influxdb database

```sh
$ influx
> use internetspeed
> select * from internet_speed
> select count(*) from internet_speed
```