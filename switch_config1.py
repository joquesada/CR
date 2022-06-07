import logging
import os
from netmiko import ConnectHandler

logging.basicConfig(filename = 'test.log', level = logging.DEBUG)
logger = logging.getLogger('netmiko')

with open ('devices') as IP_LIST:
    for IP in IP_LIST:
        SWITCH = {
              'device_type': 'cisco_nxos_ssh',
              'ip': IP,
              'username': 'admin',
              'password': 'VMware1!',
        }
        print('###Connecting to ' + IP)
        connect = ConnectHandler(**SWITCH)
                  
        with open('switch_configuration.txt') as commands:
            config = commands.read()
        output = connect.send_command(config, cmd_verify=False)
        print(output)

        output = connect.send_command('sh vlan brief')
        print(output)
