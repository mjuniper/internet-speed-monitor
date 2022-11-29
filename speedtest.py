import os
from dotenv import load_dotenv
import subprocess
import json
from influxdb import InfluxDBClient

# -s 28690 tells it to use the Fort Collins Connexion server
response = subprocess.Popen('/usr/bin/speedtest --accept-license --accept-gdpr -s 28690 --format=json', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
data = json.loads(response)

download = round(data["download"]["bandwidth"] * 0.000008, 2)
upload = round(data["upload"]["bandwidth"] * 0.000008, 2)
ping = round(data["ping"]["latency"], 2)
jitter = round(data["ping"]["jitter"], 2)

# print(download)
# print(upload)
# print(ping)
# print(jitter)

load_dotenv()
table = os.getenv('TABLE')

speed_data = [
    {
        "measurement" : table,
        "tags" : {
            "host": "pi-anemoi"
        },
        "fields" : {
            "download": float(download),
            "upload": float(upload),
            "ping": float(ping),
            "jitter": float(jitter)
        }
    }
]

host = os.getenv('HOST')
port = os.getenv('PORT')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')
client = InfluxDBClient(host, port, username, password, database)

client.write_points(speed_data)
