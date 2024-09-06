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
CLOS = graphviz.Digraph('TMF_Architecture_Team', filename='Diagram_USSVL.pdf',
                        node_attr={'color': 'lightblue2', 'style': 'filled'})
CLOS.attr(size='6,6')
CLOS.attr(ratio='0.2')

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
    Receives a list of dictionaries from the format_yaml function. Each element (dictionary) within
    the list is passed to the map function for establishing asynchronous SSH sessions to each device. Threadpool count can be adjusted
    to increase SSH session count.
    '''
    if __name__ == "__main__":
        with ThreadPool(2) as x:
            x.map(session_handler, f)

    print(time.time())
    return


def session_handler(device):
    '''
    Establishes an SSH session to the host passed into the session_handler function.
    '''

    host_vars = {
        "host": device['host'],
        "device_type": device['device_type'],
        #"username": device['username'],
        #"password": device['password'],
        "username": USERNAME,
        "password": PASSWORD,
        }

    try:
        device_host = host_vars['host']
        print('##### Connecting to ' + device['host'] + ' #####')
        net_connect = netmiko.ConnectHandler(**host_vars)

# JUMP_SERVER = {
# "host": "10.160.1.10",
# "device_type": "linux",
# "username": USERNAME,
# "password": PASSWORD,
# "session_log": 'netmiko_session.log'
# }

# try:
#     net_connect = netmiko.ConnectHandler(**JUMP_SERVER)
#     net_connect.disconnect()

# except Exception as e:
#         print(e, '\n')
#         sys.exit()

# def format_yaml(file):
#     '''
#     Loads a yaml file and formats each host into a list of dictionaries which contain the host and device type
#     for passing into the NetMiko ConnectHandler in the session_handler function.
#     '''

#     hosts = yaml.load(open('device_list.yml'), Loader=yaml.SafeLoader)
#     device_list = []

#     for host in hosts["hosts"]:
#         device_list.append(host)
#     main_loader(device_list)
    
#     return

# def main_loader(f):
#     '''
#     Receives a list of dictionaries from the format_yaml function. Threadpool count can be adjusted
#     to accommodate for more SSH sessions.
#     '''
#     if __name__ == "__main__":
#         with ThreadPool(2) as x:
#             x.map(session_handler, f)
#     print(time.time())
#     return

# def session_handler(device):
#     '''
#     Establishes an SSH session to a proxy server listed in the jump server variable, then 
#     opens an SSH session to the host contained in the dictionary that is passed to this function.
#     '''
#     net_device = device['device_type']
#     host_write = ('ssh ' + USERNAME + '@' + device['host'] + '\n')
#     vendors = ['cisco_xr', 'cisco_ios', 'juniper', 'linux', 'cisco_nxos_ssh']

#     if device['host'] != ('') and device['device_type'] in vendors:

#         try:
#             net_connect = netmiko.ConnectHandler(**JUMP_SERVER, timeout=5)

#         except Exception as e:
#             print(e, '\n')
#             return

#     elif device['host'] != ('') and device['device_type'] not in vendors:
#         print("No matching device type found for " + device['host'])
#         return

#     print("Proxy prompt ## {}".format(net_connect.find_prompt()))

#     if device['username'] != None:

#         net_connect.write_channel('ssh ' + device['username'] + '@' + device['host'] + '\n')
#         time.sleep(7)
#         output = net_connect.read_channel()

#         if 'ssword' in output:

#             check_host = net_connect.read_channel()

#             if 'Permission denied' in check_host:
#                 print('Permission denied for ' + device['host'])
#                 net_connect.disconnect()
#                 return
#             else:
#                 print('Logging into: ' + device['host'])
            
#         elif '(yes/no)?' in output:
#             net_connect.write_channel('yes\n')
#             time.sleep(2)
#             net_connect.write_channel(net_connect.password + '\n')
#             print('Logging into: ' + device['host'])
#         elif 'Could not resolve' in output:
#             print(device['host'] + ' could not be resolved, check the hostname is correct.')
#             net_connect.disconnect()
#             return
#         elif output == None:
#             print(device['host'] + " is not responding.")
#             net_connect.disconnect()
#             return
#         else:
#             print('Unknown error for ' + device['host'])
#             net_connect.disconnect()
#             return

#     else:

#         net_connect.write_channel(host_write)
#         time.sleep(7)
#         output = net_connect.read_channel()

#         if 'ssword' in output:

#             net_connect.write_channel(net_connect.password + '\n')
#             time.sleep(4)
#             check_host = net_connect.read_channel()

#             if 'Permission denied' in check_host:
#                 print('Permission denied for ' + device['host'])
#                 net_connect.disconnect()
#                 return

#             else:
#                 print('Logging into: ' + device['host'])
            
#         elif '(yes/no)?' in output:
#             net_connect.write_channel('yes\n')
#             time.sleep(2)
#             net_connect.write_channel(net_connect.password + '\n')
#             print('Logging into: ' + device['host'])
#         elif 'Could not resolve' in output:
#             print(device['host'] + ' could not be resolved, check the hostname is correct.')
#             net_connect.disconnect()
#             return
#         elif output == None:
#             print(device['host'] + " is not responding.")
#             net_connect.disconnect()
#             return
#         else:
#             print('Unknown error for ' + device['host'])
#             net_connect.disconnect()
#             return

#     netmiko.redispatch(net_connect, device_type=net_device)
    
#     if net_device == 'cisco_nxos_ssh':

#         try:

#         #     if 'spine' in device['host']:

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
