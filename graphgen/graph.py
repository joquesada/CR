import netmiko
import getpass
import sys
import time
import yaml
import re
import traceback
import graphviz
import json
from multiprocessing.pool import ThreadPool

USERNAME = input("Enter Username: ")
PASSWORD = getpass.getpass()
CLOS = graphviz.Digraph('DCMetro', filename='clos.gv',
                        node_attr={'color': 'lightblue2', 'style': 'filled'})
CLOS.attr(size='6,6')
CLOS.attr(ratio='0.2')

JUMP_SERVER = {
"host": "10.253.69.55",
"device_type": "linux",
"username": USERNAME,
"password": PASSWORD,
"session_log": 'netmiko_session.log'
}

try:
    net_connect = netmiko.ConnectHandler(**JUMP_SERVER)
    net_connect.disconnect()

except Exception as e:
        print(e, '\n')
        sys.exit()

def format_yaml(file):
    '''
    Loads a yaml file and formats each host into a list of dictionaries which contain the host and device type
    for passing into the NetMiko ConnectHandler in the session_handler function.
    '''

    hosts = yaml.load(open('device_list.yml'), Loader=yaml.SafeLoader)
    device_list = []

    for host in hosts["hosts"]:
        device_list.append(host)
    main_loader(device_list)
    
    return

def main_loader(f):
    '''
    Receives a list of dictionaries from the format_yaml function. Threadpool count can be adjusted
    to accommodate for more SSH sessions.
    '''
    if __name__ == "__main__":
        with ThreadPool(6) as x:
            x.map(session_handler, f)

    print(time.time())
    return

def session_handler(device):

    '''
    Sets up an SSH channel to the device passed into session_handler and executes show commands to extract data for building the GV graph
    '''
    net_device = device['device_type']
    vendors = ['cisco_xr', 'cisco_ios', 'juniper', 'linux', 'cisco_nxos_ssh']

    host_vars = {
        "host": device['host'],
        "device_type": device['device_type'],
        "username": USERNAME,
        "password": PASSWORD
        }

    if device['host'] != ('') and device['device_type'] in vendors:

        try:
            net_connect = netmiko.ConnectHandler(**host_vars, timeout=5)

        except Exception as e:

            with open('log_file.log', 'a') as f:
                print("Creating error log", file = f)
                f.write(device['host'] + ': ')
                traceback.print_exc(file=f)

            print(e, '\n')
            return


    elif device['host'] != ('') and device['device_type'] not in vendors:
        print("No matching device type found for " + device['host'])
        return
    
    if net_device == 'cisco_nxos_ssh':

        try:

            if 'spine' in device['host']:

                interface_count = []

                print('Verifying OSPF neighbors on ' + device['host'])    
                ospf_neighbor = net_connect.send_command('show ip ospf neighbors summary')
                read_neighbor = re.findall(r'Eth\d+/\d+', ospf_neighbor)

                for int in read_neighbor:

                    interface_count.append(int)

                for interface in interface_count:

                    line_data = net_connect.send_command('show cdp neighbors interface ' + interface + ' | egrep -A 1 "Device-ID" | exclude Device-ID')
                    read_cdp = re.findall(r'^[^.|(]*', line_data)

                    CLOS.edge(device['host'], read_cdp[0], label=interface, len='1.00')

            elif 'border' in device['host']:

                print('Verifying CDP neighbors on ' + device['host']) 
                cdp_parse = json.loads(net_connect.send_command('show cdp neighbors | json'))

                for i in cdp_parse['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_brief_info']:

                    trunc_eth = ''

                    if 'Ethernet' in i['intf_id']:

                        trunc_eth = i['intf_id'].replace('Ethernet', 'Eth')
                    else:

                        trunc_eth = i['intf_id']

                    if '.' in i['device_id']:

                        strip_domain = re.findall(r'^[^.]*', i['device_id'])
                        CLOS.edge(device['host'], strip_domain[0], label=trunc_eth, len='1.00')
                        
                    elif '(' in i['device_id']:

                        strip_serial = re.findall(r'^[^(]*', i['device_id'])
                        CLOS.edge(device['host'], strip_serial[0], label=trunc_eth, len='1.00')

                    else:

                        CLOS.edge(device['host'], i['device_id'], label=trunc_eth, len='1.00')
                
        except Exception as e:

            with open('log_file.log', 'a') as f:

                print("Creating error log", file = f)
                f.write(device['host'] + ': ')
                traceback.print_exc(file=f)

            print("Error - " + device['host'])
            net_connect.disconnect()
            return

        print("Closing connection to " + device['host'])
        net_connect.disconnect()
        return

    else:

        print("Check device_type for " + device['host'] + '. Logging out.')
        net_connect.disconnect()
        return

format_yaml('device_list.yml')
CLOS.view()
