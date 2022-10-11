import logging
import os
from netmiko import ConnectHandler

logging.basicConfig(filename = 'ITCM-47484.log', level = logging.DEBUG)
logger = logging.getLogger('netmiko')

Network_Device = {"host": "10.188.7.125",
                   "username": "svc.dcmetroscript",
                   "password": "H6@!Sd9h3Z^c67!TQbd",
                   "device_type":"cisco_nxos",
    }

print("Initiating SSH into n9k39-leaf-sjc05")
c = ConnectHandler(**Network_Device)
c.enable()
print("Initiating the configuration of the physical interfaces")
command = c.send_command_timing('conf t\n')
for (a,b,d) in zip(range(27,38),range(12,23),range(25,36)):
    command = c.send_command_timing('interface ethernet 1/' + str(a) + '\n')
    command = c.send_command_timing('description SC2-SPLUNK7-ESXi' + str(b) + ' PORT1 TKT5796009' + '\n')
    command = c.send_command_timing('channel-group ' + str(d) + ' force mode active' + '\n')
  

print("done")
print("Initiating configuration of the Port Channels")

for (x,y) in zip(range(25,36),range(12,23)):
    command = c.send_command_timing('interface port-channel' + str(x) + '\n')
    command = c.send_command_timing('shutdown' + '\n')
    command = c.send_command_timing('description SC2-SPLUNK7-ESXi' + str(y) + ' TKT5796009' + '\n')
    command = c.send_command_timing('switchport' + '\n')
    command = c.send_command_timing('switchport mode trunk' + '\n')
    command = c.send_command_timing('switchport trunk allowed vlan 1000-1001,1005-1007,1011-1013,1015,1021-1026,1029,1032-1034,1037,1046,1048,1058,1073-1078' + '\n')
    command = c.send_command_timing('switchport trunk allowed vlan add 1102,1505-1506,1509,1522,1524,1526,1531-1532,1534-1535,1537,1542,1546,1600-1602,1901-1906,1909,2104-2109,2112,2201-2202,2214-2217,2280' + '\n')
    command = c.send_command_timing('spanning-tree port type edge trunk ' + '\n')
    command = c.send_command_timing('mtu 9216' + '\n')
    command = c.send_command_timing('no lacp suspend-individual' + '\n')
    command = c.send_command_timing('vpc ' + str(x) + '\n')
    command = c.send_command_timing('no shutdown' + '\n')

print("Config is completed, saving config")

command = c.send_command_timing('end' + '\n')
command = c.send_command_timing('copy r s' + '\n')

c.disconnect()

Network_Device2 = {"host": "10.188.7.126",
                   "username": "svc.dcmetroscript",
                   "password": "H6@!Sd9h3Z^c67!TQbd",
                   "device_type":"cisco_nxos",
    }

print("Initiating SSH into n9k40-leaf-sjc05")
c = ConnectHandler(**Network_Device2)
c.enable()
print("Initiating the configuration of the physical interfaces")
command = c.send_command_timing('conf t\n')
for (a,b,d) in zip(range(27,38),range(12,23),range(25,36)):
    command = c.send_command_timing('interface ethernet 1/' + str(a) + '\n')
    command = c.send_command_timing('description SC2-SPLUNK7-ESXi' + str(b) + ' PORT2 TKT5796009' + '\n')
    command = c.send_command_timing('channel-group ' + str(d) + ' force mode active' + '\n')
  

print("done")
print("Initiating configuration of the Port Channels")

for (x,y) in zip(range(25,36),range(12,23)):
    command = c.send_command_timing('interface port-channel' + str(x) + '\n')
    command = c.send_command_timing('shutdown' + '\n')
    command = c.send_command_timing('description SC2-SPLUNK7-ESXi' + str(y) + ' TKT5796009' + '\n')
    command = c.send_command_timing('switchport' + '\n')
    command = c.send_command_timing('switchport mode trunk' + '\n')
    command = c.send_command_timing('switchport trunk allowed vlan 1000-1001,1005-1007,1011-1013,1015,1021-1026,1029,1032-1034,1037,1046,1048,1058,1073-1078' + '\n')
    command = c.send_command_timing('switchport trunk allowed vlan add 1102,1505-1506,1509,1522,1524,1526,1531-1532,1534-1535,1537,1542,1546,1600-1602,1901-1906,1909,2104-2109,2112,2201-2202,2214-2217,2280' + '\n')
    command = c.send_command_timing('spanning-tree port type edge trunk ' + '\n')
    command = c.send_command_timing('mtu 9216' + '\n')
    command = c.send_command_timing('no lacp suspend-individual' + '\n')
    command = c.send_command_timing('vpc ' + str(x) + '\n')
    command = c.send_command_timing('no shutdown' + '\n')

print("Config is completed, saving config")

command = c.send_command_timing('end' + '\n')
command = c.send_command_timing('copy r s' + '\n')

c.disconnect()


Network_Device3 = {"host": "10.188.7.177",
                   "username": "svc.dcmetroscript",
                   "password": "H6@!Sd9h3Z^c67!TQbd",
                   "device_type":"cisco_nxos",
    }

print("Initiating SSH into access01-mgmt-sjc05")
c = ConnectHandler(**Network_Device3)
c.enable()
print("Initiating the configuration of the physical interfaces")
command = c.send_command_timing('conf t\n')
for d in range(2,13):
    command = c.send_command_timing('interface ethernet 184/1/' + str(d) + '\n')
    command = c.send_command_timing('switchport access vlan 100' + '\n')
    command = c.send_command_timing('no shutdown' + '\n')

print("Config is completed, saving config")

command = c.send_command_timing('end' + '\n')
command = c.send_command_timing('copy r s' + '\n')

c.disconnect()

Network_Device4 = {"host": "10.188.7.176",
                   "username": "svc.dcmetroscript",
                   "password": "H6@!Sd9h3Z^c67!TQbd",
                   "device_type":"cisco_nxos",
    }

print("Initiating SSH into access02-mgmt-sjc05")
c = ConnectHandler(**Network_Device4)
c.enable()
print("Initiating the configuration of the physical interfaces")
command = c.send_command_timing('conf t\n')
for e in range(2,13):
    command = c.send_command_timing('interface ethernet 184/1/' + str(e) + '\n')
    command = c.send_command_timing('switchport access vlan 100' + '\n')
    command = c.send_command_timing('no shutdown' + '\n')

print("Config is completed, saving config")

command = c.send_command_timing('end' + '\n')
command = c.send_command_timing('copy r s' + '\n')

c.disconnect()

print("done")
