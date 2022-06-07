
from netmiko import ConnectHandler
import time
import datetime

time = datetime.datetime.now().replace(microsecond=0)

IP_LIST = open('devices')
for IP in IP_LIST:
    switches = {
        'device_type':'cisco_nxos_ssh',
        'ip': IP,
        'username':'admin',
        'password':'VMware1!',
    }

    print('###Connecting to ' + IP)
    conn = ConnectHandler(**switches)

    print('\n Backing up configuration\n')
    output = conn.send_command('sh run')
    save_file = open('Switch_' + IP + str(time), 'w')
    save_file.write(output)
    save_file.close
    print('\n Finished backup \n')
