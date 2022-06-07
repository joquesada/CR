from netmiko import ConnectHandler
import logging
import yaml
import time
from multiprocessing.pool import ThreadPool
import getpass

logging.basicConfig(filename = 'results.log', level = logging.DEBUG)
logger = logging.getLogger('netmiko')

#USERNAME = input("Enter username: ")
#PASSWORD = getpass.getpass()


def format_yaml(file):
    hosts = yaml.load(open('devices.yml'), Loader=yaml.SafeLoader)
    devices = []

    for host in hosts["hosts"]:
        devices.append(host)


    multitre(devices)

    return


def multitre(f):

    if __name__ =="__main__":
        with ThreadPool(1) as x:
            x.map(session, f)

    #print(time.time())
    return


def session(device):

    host_vars = {
        "host": device['host'],
        "device_type": device['device_type'],
        #"username": USERNAME,
        #"password": PASSWORD,
        "username": device['username'],
        "password": device['password'],
        }


    try:
        device_host = host_vars['host']
        print('#### Connecting to ' + device['host'] + ' ####')
        net_connect = ConnectHandler(**host_vars)

        command = net_connect.send_command_timing('conf t')
        command = net_connect.send_command_timing('cli alias name wr copy running-config startup-config')
        command = net_connect.send_command_timing('end')
        command = net_connect.send_command_timing('copy r s')
        print('#### Successful - ' + device['host'] + ' - closing connection ###')
        net_connect.disconnect()
        return

    except Exception as e:
        print(e)
        return

format_yaml('devices.yml')
