import logging
import os
from netmiko import ConnectHandler

logging.basicConfig(filename = 'test.log', level = logging.DEBUG)
logger = logging.getLogger('netmiko')

Network_Device = {"host": "10.10.10.10",
                   "username": "admin",
                   "password": "VMware1!",
                   "device_type":"cisco_nxos",
    }

print("Initiating SSH into the device")
c = ConnectHandler(**Network_Device)
c.enable()
print("Initiating the configuration of the physical interfaces")
command = c.send_command_timing('conf t\n')
for (a,b,d) in zip(range(35,39),range(1,5),range(32,36)):
    command = c.send_command_timing('interface ethernet 1/' + str(a) + '\n')
    command = c.send_command_timing('description WDC-PROD54-ESXi0' + str(b) + ' PORT1 TKT5329652' + '\n')
    command = c.send_command_timing('channel-group ' + str(d) + ' mode active' + '\n')
  

print("done")
print("Initiating configuration of the Port Channels")

for (x,y) in zip(range(32,36),range(1,5)):
    command = c.send_command_timing('interface port-channel' + str(x) + '\n')
    command = c.send_command_timing('shutdown' + '\n')
    command = c.send_command_timing('description WDC-PROD54-ESXi0' + str(y) + ' TKT5329652' + '\n')
    command = c.send_command_timing('switchport' + '\n')
    command = c.send_command_timing('switchport mode trunk' + '\n')
    command = c.send_command_timing('switchport trunk allowed vlan 40,42,141,1023,1610,2900' + '\n')
    command = c.send_command_timing('switchport trunk allowed vlan add 3155,3156,3161,3162' + '\n')
    command = c.send_command_timing('spanning-tree port type edge trunk ' + '\n')
    command = c.send_command_timing('mtu 9216' + '\n')
    command = c.send_command_timing('no lacp suspend-individual' + '\n')
    command = c.send_command_timing('vpc ' + str(x) + '\n')
    command = c.send_command_timing('no shutdown' + '\n')

print("Config is completed, saving config")

command = c.send_command_timing('end' + '\n')
command = c.send_command_timing('copy r s' + '\n')

c.disconnect()

print("done")


