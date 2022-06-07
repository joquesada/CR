import os
from netmiko import ConnectHandler
from pprint import pprint
import json

Network_Device = {"host": "10.10.10.11",
                   "username": "admin",
                   "password": "VMware1!",
                   "device_type":"cisco_nxos",
    }


user_cmd = input(str('Enter command:'))
c = ConnectHandler(**Network_Device)
c.enable()
command = c.send_command(user_cmd, use_textfsm=True)
print(command)



