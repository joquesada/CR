import os
from netmiko import ConnectHandler
from pprint import pprint
import json

Network_Device = {"host": "10.128.166.4",
                   "username": "jquesada",
                   "password": "Cowintapate23",
                   "device_type":"cisco_nxos",
    }


try:
    c = ConnectHandler(**Network_Device)
    c.enable()
    command = c.send_command('sh ip int br', use_textfsm=True)
    #print(json.dumps(version, indent=2))
    #for hostname in version:
     #   for os in version:
        #for uptime in version:
      #  if interface['status'] == 'down':
            #print(f"{hostname['hostname']} uptime is: {uptime['uptime']}")
            #print(f"{hostname['hostname']} nxos version is: {os['os']}")
    #pprint(version)
    for intf in command:
        #print(f"Interface: {intf['intf']}")
        for ipaddr in command:
        #print(f"IP: {ipaddr['ipaddr']}")
            for link in command:
        #print(f"Link Status: {link['link']}")
                print(f"Interface:{intf['intf']}, IP:{ipaddr['ipaddr']}, Link Status: {link['link']}")
   # c.close()
except Exception as e:
    print(e)
