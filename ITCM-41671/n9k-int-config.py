import logging
import os
from netmiko import ConnectHandler

logging.basicConfig(filename = 'test.log', level = logging.DEBUG)
logger = logging.getLogger('netmiko')

Network_Device = {"host": "10.128.166.2",
                   "username": "svc.dcmetroscript",
                   "password": "Kp!@9z2@EdSp3F1p.^R",
                   "device_type":"cisco_nxos",
    }

print("Initiating SSH into n9k29")
c = ConnectHandler(**Network_Device)
c.enable()
print("Initiating the configuration of the physical interfaces")
command = c.send_command_timing('conf t\n')
for a in range(21,33):
    command = c.send_command_timing('interface ethernet 1/' + str(a) + '\n')
    command = c.send_command_timing('switchport' + '\n')
    command = c.send_command_timing('switchport mode trunk' + '\n')
    command = c.send_command_timing('switchport trunk allowed vlan 3817-3835,3854,3856' + '\n')
    command = c.send_command_timing('spanning-tree port type edge trunk ' + '\n')
    command = c.send_command_timing('mtu 9216' + '\n')
    command = c.send_command_timing('no shutdown' + '\n')

print("Config is completed, saving config")

command = c.send_command_timing('end' + '\n')
command = c.send_command_timing('copy r s' + '\n')

c.disconnect()

Network_Device1 = {"host": "10.128.166.3",
                   "username": "svc.dcmetroscript",
                   "password": "Kp!@9z2@EdSp3F1p.^R",
                   "device_type":"cisco_nxos",
    }

print("Initiating SSH into n9k30")
c = ConnectHandler(**Network_Device1)
c.enable()
print("Initiating the configuration of the physical interfaces")
command = c.send_command_timing('conf t\n')
for b in range(21,33):
    command = c.send_command_timing('interface ethernet 1/' + str(b) + '\n')
    command = c.send_command_timing('switchport' + '\n')
    command = c.send_command_timing('switchport mode trunk' + '\n')
    command = c.send_command_timing('switchport trunk allowed vlan 3817-3835,3854,3856' + '\n')
    command = c.send_command_timing('spanning-tree port type edge trunk ' + '\n')
    command = c.send_command_timing('mtu 9216' + '\n')
    command = c.send_command_timing('no shutdown' + '\n')

print("Config is completed, saving config")

command = c.send_command_timing('end' + '\n')
command = c.send_command_timing('copy r s' + '\n')

c.disconnect()

Network_Device3 = {"host": "10.250.201.33",
                   "username": "svc.dcmetroscript",
                   "password": "Kp!@9z2@EdSp3F1p.^R",
                   "device_type":"cisco_nxos",
    }

print("Initiating SSH into core01-mgmt")
c = ConnectHandler(**Network_Device3)
c.enable()
print("Initiating the configuration of the physical interfaces")
command = c.send_command_timing('conf t\n')
for d in range(32,44):
    command = c.send_command_timing('interface ethernet 181/1/' + str(d) + '\n')
    command = c.send_command_timing('switchport access vlan 3856' + '\n')
    command = c.send_command_timing('no shutdown' + '\n')

print("Config is completed, saving config")

command = c.send_command_timing('end' + '\n')
command = c.send_command_timing('copy r s' + '\n')

c.disconnect()

Network_Device4 = {"host": "10.250.201.34",
                   "username": "svc.dcmetroscript",
                   "password": "Kp!@9z2@EdSp3F1p.^R",
                   "device_type":"cisco_nxos",
    }

print("Initiating SSH into core02-mgmt")
c = ConnectHandler(**Network_Device4)
c.enable()
print("Initiating the configuration of the physical interfaces")
command = c.send_command_timing('conf t\n')
for e in range(32,44):
    command = c.send_command_timing('interface ethernet 181/1/' + str(e) + '\n')
    command = c.send_command_timing('switchport access vlan 3856' + '\n')
    command = c.send_command_timing('no shutdown' + '\n')

print("Config is completed, saving config")

command = c.send_command_timing('end' + '\n')
command = c.send_command_timing('copy r s' + '\n')

c.disconnect()

print("done")
