from netmiko import ConnectHandler
import logging
import os
import json
import time
import yaml
import getpass
import sys
from multiprocessing.pool import ThreadPool

logging.basicConfig(filename = 'ITCM-42680.log', level = logging.DEBUG)
logger = logging.getLogger('netmiko')

#USERNAME = input("Enter Username: ")
#PASSWORD = getpass.getpass()

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
        with ThreadPool(4) as x:
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
        "username": device['username'],
        "password": device['password'],
        #"username": USERNAME,
        #"password": PASSWORD,
        }

    try:
        device_host = host_vars['host']
        print('##### Connecting to ' + device['host'] + ' #####')
        net_connect = ConnectHandler(**host_vars)
        
        command = net_connect.send_command_timing('conf t')
        command = net_connect.send_command_timing('username admin password 5 $5$FGNONO$mhH1sRVog92G6Gf4Zyo83aRmq92Mys44LFU7MyiFs52')
        command = net_connect.send_command_timing('end')
        command = net_connect.send_command_timing('copy running-config startup-config')
        net_connect.disconnect()
        print('##### Successful - ' + device['host'] + ' - Closing connection #####')
        return

    except Exception as e:
        print(e)
        return


format_yaml('device_list.yml')
