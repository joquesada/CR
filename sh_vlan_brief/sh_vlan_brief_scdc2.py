from netmiko import ConnectHandler
import json
import time
import yaml
import getpass
import sys
from multiprocessing.pool import ThreadPool

#USERNAME = input("Enter Username: ")
#PASSWORD = getpass.getpass()
VLAN_FILE = 'vlan_brief_scdc2.csv'

JUMP_SERVER = {
"host": "10.253.69.55",
"device_type": "linux",
#"username": USERNAME,
#"password": PASSWORD,
"username": "svc.dcmetroscript",
"password": "Kp!@9z2@EdSp3F1p.^R",
"session_log": 'netmiko_session2.log'
}

# Test credentials on a single host prior to multithreading. Exit the script upon authentication failure.
#try:
#    print("Verifying credentials on " + JUMP_SERVER['host'])
#    net_connect = ConnectHandler(**JUMP_SERVER)
#    net_connect.disconnect()
#    print("Authentication Successful...")

#except Exception as e:
#        print(e, '\n')
#        sys.exit()

# Default the VLAN file on execution
with open(VLAN_FILE, 'w') as f:
    f.write('Device,VLAN,Name' + '\n')

def format_yaml(file):
    '''
    Loads a yaml file and formats each host into a list of dictionaries which contain the host and device type
    for passing into the NetMiko ConnectHandler in the session_handler function.
    '''

    hosts = yaml.load(open('device_list_scdc2.yml'), Loader=yaml.SafeLoader)
    device_list = []

    for host in hosts["hosts"]:
        device_list.append(host)

    main_loader(device_list)

    return

def main_loader(f):
    '''
    Receives a list of dictionaries from the format_yaml function. Each element (dictionary) within
    the list is passed to the map function for establishing asynchronous SSH sessions to each device. Threadpool count can be adjusted
    to increase SSH session count.
    '''
    if __name__ == "__main__":
        with ThreadPool(4) as x:
            x.map(session_handler, f)

    print(time.time())
    return

def int_recurse(int, device):
    for key,value in int.items():
        if isinstance(value, dict):
            int_recurse(value, device)
        elif isinstance(value, list):
            for i in value:
                with open(VLAN_FILE, 'a') as w:
                    #if 'prefix' in i:
                    w.write(device + ',' + i['vlanshowbr-vlanid'] + ',' + i['vlanshowbr-vlanname'] + '\n')
                    #else:
                     #   w.write(device + ',' + i['vrf-name-out'] + ',' + i['intf-name'] + ',' + i['link-state'] + '\n')
        else:
            print(key, value)
    return

def session_handler(device):
    '''
    Establishes an SSH session to the host passed into the session_handler function.
    '''

    host_vars = {
        "host": device['host'],
        "device_type": device['device_type'],
        "username": device['username'],
        "password": device['password'],
        #"username": USERNAME,
        #"password": PASSWORD,
        "session_log": 'netmiko_session2.log'
        }

    try:
        device_host = host_vars['host']
        print('##### Connecting to ' + device['host'] + ' #####')
        net_connect = ConnectHandler(**host_vars)

        int_parse = json.loads(net_connect.send_command('sh vlan brief | json'))
        int_recurse(int_parse, device_host)
        net_connect.disconnect()
        print('##### Successful - ' + device['host'] + ' - Closing connection #####')
        return

    except Exception as e:
        print(e)
        return


format_yaml('device_list_scdc2.yml')
