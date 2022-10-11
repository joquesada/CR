import logging
import os
from netmiko import ConnectHandler

logging.basicConfig(filename = 'ITCM-45585.log', level = logging.DEBUG)
logger = logging.getLogger('netmiko')

Network_Device = {"host": "10.10.10.10",
                   "username": "admin",
                   "password": "VMware1!",
                   "device_type":"cisco_nxos",
    }

print("Initiating SSH into n9k01-leaf-eat1")
c = ConnectHandler(**Network_Device)
c.enable()
print("Initiating the configuration of the physical interfaces")
command = c.send_command_timing('conf t\n')
for (a,b,d) in zip(range(35,45),range(1,11),range(118,129)):
    command = c.send_command_timing('interface ethernet 1/' + str(a) + '\n')
    command = c.send_command_timing('description WDC-BZ11NSX-ESXi0' + str(b) + ' PORT1 TKT5930002' + '\n')
    command = c.send_command_timing('channel-group ' + str(d) + ' force mode active' + '\n')
  

print("done")
print("Initiating configuration of the Port Channels")

for (x,y) in zip(range(118,129),range(1,11)):
    command = c.send_command_timing('interface port-channel' + str(x) + '\n')
    command = c.send_command_timing('shutdown' + '\n')
    command = c.send_command_timing('description WDC-BZ11-ESXi0' + str(y) + ' TKT5930002' + '\n')
    command = c.send_command_timing('switchport' + '\n')
    command = c.send_command_timing('switchport mode trunk' + '\n')
    command = c.send_command_timing('switchport trunk allowed vlan 2901-2937' + '\n')
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
