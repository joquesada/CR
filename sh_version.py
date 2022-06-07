import os
from netmiko import ConnectHandler
from pprint import pprint
import json

Network_Device = {"host": "10.10.10.10",
                   "username": "admin",
                   "password": "VMware1!",
                   "device_type":"cisco_nxos",
    }


try:
    c = ConnectHandler(**Network_Device)
    c.enable()
    version = c.send_command('sh version', use_textfsm=True)
#    print(json.dumps(version, indent=2))
    for hostname in version:
        for os in version:
            for uptime in version:
                print(f"{hostname['hostname']} uptime is: {uptime['uptime']}")
                print(f"{hostname['hostname']} nxos version is: {os['os']}")
#    pprint(version)
 #   c.close()
except Exception as e:
    print(e)
