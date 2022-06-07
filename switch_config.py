import os
from netmiko import ConnectHandler

with open ('devices') as IP_LIST:
    for IP in IP_LIST:
        DEVICE = {
                'device_type': 'cisco_nxos_ssh',
		'ip': IP,
		'username': 'admin',
		'password': 'VMware1!',
	}

        print('###Connecting to:' + IP)
        connect = ConnectHandler(**DEVICE)

        with open("switch_configuration.txt") as config_commands:
            config = config_commands.read()
        output = connect.send_config_set(config, cmd_verify=False)
        print(output)

        output1 = connect.send_command('sh int eth 1/57 - 58 description')
        print(output1)

