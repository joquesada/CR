import logging
import os
from netmiko import ConnectHandler

logging.basicConfig(filename = 'ITCM-47973.log', level = logging.DEBUG)
logger = logging.getLogger('netmiko')

Network_Device3 = {"host": "10.250.201.33",
                   "username": "svc.dcmetroscript",
                   "password": "H6@!Sd9h3Z^c67!TQbd",
                   "device_type":"cisco_nxos",
    }

print("Initiating SSH into core01-mgmt-eat1")
c = ConnectHandler(**Network_Device3)
c.enable()
print("Initiating the configuration of the physical interfaces")
command = c.send_command_timing('conf t\n')
for (f,d) in zip(range(12,23),range(32,43)):
    command = c.send_command_timing('interface ethernet 180/1/' + str(d) + '\n')
    command = c.send_command_timing('description WDC-SPLUNK7-ESXi' + str(f) + ' - IDR TKT5796014' + '\n')
    command = c.send_command_timing('switchport access vlan 3856' + '\n')
    command = c.send_command_timing('no shutdown' + '\n')

print("Config is completed, saving config")

command = c.send_command_timing('end' + '\n')
command = c.send_command_timing('copy r s' + '\n')

c.disconnect()

Network_Device4 = {"host": "10.250.201.34",
                   "username": "svc.dcmetroscript",
                   "password": "H6@!Sd9h3Z^c67!TQbd",
                   "device_type":"cisco_nxos",
    }

print("Initiating SSH into core02-mgmt-eat1")
c = ConnectHandler(**Network_Device4)
c.enable()
print("Initiating the configuration of the physical interfaces")
command = c.send_command_timing('conf t\n')
for (g,e) in zip(range(12,23),range(32,43)):
    command = c.send_command_timing('interface ethernet 180/1/' + str(e) + '\n')
    command = c.send_command_timing('description WDC-SPLUNK7-ESXi' + str(g) + ' - IDR TKT5796014' + '\n')
    command = c.send_command_timing('switchport access vlan 100' + '\n')
    command = c.send_command_timing('no shutdown' + '\n')

print("Config is completed, saving config")

command = c.send_command_timing('end' + '\n')
command = c.send_command_timing('copy r s' + '\n')

c.disconnect()

print("done")
