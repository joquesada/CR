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
print('\n Output from Device\n')
output = net_connect.send_command('sh ip int br', use_textfsm=True)
print(output)

print('\n Output using FOR Loop and IF \n')
devlist = []
for i in output:
    if i['status'] == 'up':
        devlist.append(i['intf'])
print(devlist)

print('\n A different way to gather the same output \n')
print([i['intf'] for i in output if i['status'] =='up'])

print('\n List of interfaces UP \n#######################')
statusup = [i['intf'] for i in output if i['status'] =='up']
for intup in statusup:
    print(intup)

print('\n List of interfaces DOWN \n#######################')
statusdown = [i['intf'] for i in output if i['status'] !='up']
for intdown in statusdown:
    print(intdown)
