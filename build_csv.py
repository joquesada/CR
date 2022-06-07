import os
from netmiko import ConnectHandler
import json
import csv

Network_Device = {"host": "10.10.10.10",
                   "username": "admin",
                   "password": "VMware1!",
                   "device_type":"cisco_nxos",
    }

version_file = "version.csv"

try:
    c = ConnectHandler(**Network_Device)
    c.enable()
    version = json.loads(c.send_command('sh version | json'))
    with open(version_file, "w") as f:
        f.write('hostname,os' + '\n')
        f.write(version['host_name']+','+version['nxos_ver_str']+ '\n')

except Exception as e:
    print(e)
