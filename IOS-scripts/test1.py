from netmiko import ConnectHandler
from getpass import getpass

RTR = {
      'device_type': 'cisco_ios',
      'host': '10.10.10.20',
      'username': 'admin',
      'password': 'VMware1!',
}

print ('\n #### Connecting to router ####')
net_connect = ConnectHandler(**RTR)
output = net_connect.send_command('sh ip int br', use_textfsm=True)
#print(output)
#print(output[0])
l = len(output)
print("Total number of interfaces is " + str(l))

name = output[0]['intf']
status = output[0]['status']
print('\n Interface ' + name + ' status is ' + status)
