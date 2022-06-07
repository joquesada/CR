import os
from netmiko import ConnectHandler

with open ('devices') as devices:
    for IP in devices:
        switches = {
                    'device_type': 'cisco_nxos_ssh',
                    'ip': IP,
                    'username':'admin',
                    'password':'VMware1!',
        }
        print('#####Connecting to' + IP)
        connect = ConnectHandler(**switches)

        with open('switch_configuration.txt') as commands:
            config = commands.read()
        output = connect.send_command(config, cmd_verify=False)
        print(output)
