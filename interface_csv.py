import os
from netmiko import ConnectHandler
import json
import csv

Network_Device = {"host": "10.10.10.10",
                   "username": "admin",
                   "password": "VMware1!",
                   "device_type":"cisco_nxos",
    }

interface_file = 'interface.csv'
fields = ["VRF","intf-name","Status"]

try:
    c = ConnectHandler(**Network_Device)
    interface1 = json.loads(c.send_command("sh ip interface br vrf all | json"))
    with open(interface_file, "w") as f:
        writer = csv.DictWriter(f, fields)
        writer.writeheader()
        for x, details in interface1.items():
            writer.writerow({"vrf-name-out": details["vrf-name-out"],
                             "intf-name": details["intf-name"],
                             "link-state": details["link-state"]})


except Exception as e:
    print(e)
