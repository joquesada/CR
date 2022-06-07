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
print(output[3])
l = len(output)
print("\n Total number of interfaces is " + str(l))

print('\n List of Interfaces which are UP \n #####################')
for i in range(0,l):
    if output[i]['status'] == 'up':
        print(' ' + output[i]['intf'] + ' --> ' + output[i]['status'])


print('\n List of Interfaces which are DOWM \n #####################')
for i in range(0,l):
    if output[i]['status'] != 'up':
        print(' ' + output[i]['intf'] + ' --> ' + output[i]['status'])
