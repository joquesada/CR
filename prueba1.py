import os
from netmiko import ConnectHandler


#lista1 = ['1','2','3','4','5']
#lista2 = ['3','4','5','6','7']

Network_Device = {"host": "10.10.10.10",
                   "username": "admin",
                   "password": "VMware1!",
                   "device_type":"cisco_nxos",
    }

#n9k01 = ConnectHandler(ip="10.10.10.10",username="admin",password="VMware1!",device_type="cisco_nxos")

#def config(n9k01):
 #   n9k01.enable()
 #   n9k01.send_command("conf t\n")
 #   n9k01.send_command("interface ethernet 1/1\n")
 #   n9k01.send_command("description test 3\n")
 #   n9k01.send_command("switchport\n")
 #   n9k01.send_command("switchport mode trunk\n")


#x = lista1
#y = lista2

#for x, y in zip(lista1, lista2):
#n9k01_config = n9k01.send_command = ("conf t" , "interface ethernet 1/1", "description test 3", "switchport", "switchport mode trunk")
#n9k01_config = n9k01.send_command("sh run int eth 1/1 - 5")
#print(n9k01_config)
#x + 1
#y + 1
    
#n9k01.disconnect()

try:
    c = ConnectHandler(**Network_Device)
    c.enable()
    command = c.send_command('conf t')
    command = c.send_command('interface ethernet 1/1')
    command = c.send_command('description test 3')
    command = c.send_command('switchport')
    command = c.send_command('switchport mode trunk')
    c.disconnect()
    exit()
