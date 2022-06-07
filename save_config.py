#!/usr/bin/env python3

import os
os.chdir("/home/lab/python3-programming/configs")
from netmiko import ConnectHandler

print("Connecting to device: n9k01")
#n9k01 = ConnectHandler(ip="10.10.10.10",username="admin",password="VMware1!",device_type="cisco_nxos")
n9k01 = ConnectHandler(ip="10.128.166.2",username="svc.dcmetroscript",password="Kp!@9z2@EdSp3F1p.^R",device_type="cisco_nxos")
n9k01.enable()

print("Saving the confioguration")
n9k01.send_command("copy r s")

print("Backing up the config")
n9k01.send_command("terminal len 0")
n9k01_config = n9k01.send_command("show run")
with open("n9k29.cfg", "w") as temp:
    temp.write(n9k01_config)

n9k01.disconnect()

print("Connecting to device: n9k02")
#n9k02 = ConnectHandler(ip="10.10.10.11",username="admin",password="VMware1!",device_type="cisco_nxos")
n9k02 = ConnectHandler(ip="10.128.166.3",username="svc.dcmetroscript",password="Kp!@9z2@EdSp3F1p.^R",device_type="cisco_nxos")
n9k02.enable()

print("Saving the confioguration")
n9k02.send_command("copy r s")

print("Backing up the config")
n9k02.send_command("terminal len 0")
n9k02_config = n9k02.send_command("show run")
with open("n9k30.cfg", "w") as temp:
    temp.write(n9k02_config)

n9k02.disconnect()

print("Backup is completed")

