import logging
import os
from netmiko import ConnectHandler

logging.basicConfig(filename = 'test.log', level = logging.DEBUG)
logger = logging.getLogger('netmiko')

Network_Device = {"host": "10.128.160.165",
                   "username": "svc.dcmetroscript",
                   "password": "Kp!@9z2@EdSp3F1p.^R",
                   "device_type":"cisco_nxos",
    }

print("Initiating SSH into n9k18")
c = ConnectHandler(**Network_Device)
c.enable()
print("Initiating the configuration of the physical interfaces")
command = c.send_command_timing('conf t\n')
for (a,b) in zip(range(21,27),range(14,25,2)):
    command = c.send_command_timing('interface ethernet 1/' + str(a) + '\n')
    command = c.send_command_timing('description WDC-CB-MACPROD-' + str(b) + ' PORT1 TKT5603121' + '\n')
    command = c.send_command_timing('switchport' + '\n')
    command = c.send_command_timing('switchport mode trunk' + '\n')
    command = c.send_command_timing('switchport trunk allowed vlan 2883' + '\n')
    command = c.send_command_timing('spanning-tree port type edge trunk ' + '\n')
    command = c.send_command_timing('mtu 9216' + '\n')
    command = c.send_command_timing('no shutdown' + '\n')

print("Config is completed, saving config")

command = c.send_command_timing('end' + '\n')
command = c.send_command_timing('copy r s' + '\n')

c.disconnect()

print("done")


