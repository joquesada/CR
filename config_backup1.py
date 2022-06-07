
from netmiko import ConnectHandler
import time
import datetime
import getpass

time = datetime.datetime.now().replace(microsecond=0)

USERNAME = input("Enter username: ")
PASSWORD = getpass.getpass()


IP_LIST = open('devices')
for IP in IP_LIST:
    switches = {
        'device_type':'cisco_nxos_ssh',
        'ip': IP,
        'username':USERNAME,
        'password':PASSWORD,
    }

    print('###Connecting to ' + IP)
    conn = ConnectHandler(**switches)

    print('\n Backing up configuration\n')
    output = conn.send_command('sh run')
    save_file = open('configs/' + 'Switch_' + IP + str(time), 'w')
    save_file.write(output)
    save_file.close
    print('\n Finished backup \n')
