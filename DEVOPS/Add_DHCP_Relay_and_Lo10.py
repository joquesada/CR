###############################################
# #### WARNING!!!! 
# ####  TO RUN THE SCRIPT NEED TO REMOVE COMMENT 
# #### FROM LINE 192  AND LINE 193 AND VERIFY HOSTS
###############################################

from ipaddress import IPv4Address, IPv4Network, ip_address, ip_network
from termcolor import cprint
from datetime import datetime
import yaml
import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler

#==============
# Define varuables 
#==============

DCname = 'WDC'
VRFname = 'Corp'

#============================================================
# Enabling Netmiko logging of all reads and writes of the communications channel
#============================================================

logging.basicConfig(filename = 'Logs/logfiles/test_dhcp_relay_check_' + DCname + '.log', level = logging.DEBUG)
logger = logging.getLogger('netmiko')

with open('Logs/logfiles/test_dhcp_relay_check_' + DCname + '.log', 'w') as f:
    f.close()

#password = getpass.getpass(stream=sys.stderr)

#===================================
# Define function to read devices from yaml file
#===================================

def list_hosts (devicefile):
 # Opening yaml file for connection to devices and read it in dictionary "file"
    with open(devicefile) as f:
        file = yaml.safe_load(f.read())

    return file

#===============================================
# Defining function for connection to the device and run commmands
#===============================================

def  Login(device):

    username = hosts['common_vars']['username']
    password = hosts['common_vars']['password']
    device_type = hosts['common_vars']['device_type']

      # Connecting to the jump server:
    device_ssh = {
            "host": device,
            "device_type": device_type,
            "username": username,
            "password": password,
            'verbose': True,
            'fast_cli': True
            }

    try:
            ssh = ConnectHandler(**device_ssh)
            output = ssh.read_channel()

            if 'ssword' in output:
                ssh.write_channel(ssh.password + '\n')

            elif '(yes/no)?' in output:
                ssh.write_channel('yes\n')
                ssh.write_channel(ssh.password + '\n')

                if 'ssword' in output:
                    ssh.read_channel()
                    ssh.write_channel(ssh.password + '\n')
                
            config_command(device,ssh)

    except Exception as error:
        print(error, '\n')
        sys.exit()

#=========================================================
# Defining function to verify router-id statically configured on leaf switches and 
# execute commands to configure the int Lo, write to the file
#=========================================================

def config_command (device,ssh):

    filename = "Logs/logfiles/bgp_ospf_router-id-" + DCname + '_' + time_now + ".txt"

    with open(filename, 'a+') as f:
        cprint('\n' + device, 'green')
        f.write ('\n' + '=' * 50 + '\n')
        f.write(device + '\n')
        f.write ('=' * 50 + '\n'*2)

            #######################################################################################
            ### LINE 159-173 - add ip dhcp relay source-interface Lo10 for SVI (vlan.yml and vlan_19.yml for leaf19/20 and verify
            ### LINE 113-131 - verify configuration bgp and ospf (router-id) and Lo10 on device
            ### LINE 133-153 - configure int Lo10 on leaf switches
            #######################################################################################

        vlans_file = yaml.load(open('yml/vlan_19.yml'), Loader=yaml.SafeLoader)
        vlans = vlans_file['vlans']
        print(vlans)

        config_file = yaml.load(open('yml/interface_IP_vlan.yml'), Loader=yaml.SafeLoader)
        intLo = config_file['interface']
        ip_subnet_conf = config_file['IP']
        print('Conifguration is preparing for the ' + intLo)
        leaf_ip_dict = {}
        for IPaddress_Lo  in IPv4Network(ip_subnet_conf):
            if device[3:5].strip('0') == str(IPaddress_Lo).split('.')[3]:
                    leaf_ip_dict[device] = IPaddress_Lo
                    cprint(leaf_ip_dict, 'blue')
                    f.write('Conifguration is preparing for the ' + intLo + " with IP address " + str(IPaddress_Lo) )
                    f.write("\n" )
                    
                    command_check = [ 'show run section bgp | egrep "bgp|vrf|router-id"',
                                                        'show bgp vrf ' + VRFname + ' process | egrep -I router',
                                                        'show run | egrep -A 1 "router ospf" | ex "area|pim|--"'
                                                        ]
                    result_command_check = ssh.send_command(command_check)
                    f.write(result_command_check)
                    f.write("\n" )
                    
                    result = ssh.send_command('show run int '+ intLo)
                    if 'Loopback' in result:
                        loopback_check_output = result
                        print(result)
                        f.write(result)
                        f.write("\n" )
                    else:
                        loopback_check_output = ' Interface ' + intLo + ' is not configured yet on leaf switch ' + device 
                        print(' Interface ' + intLo + ' is not configured yet on leaf switch ' + device )
                        f.write( ' Interface ' + intLo + ' is not configured yet on leaf switch ' + device )
                        print(' Interface ' + intLo + ' is configuring now on leaf switch ' + device )
                        f.write( ' Interface ' + intLo + ' is configuring now on leaf switch ' + device )
                        f.write("\n" )
                        command = ['interface ' + intLo,
                                                'vrf member ' + VRFname,
                                                'ip address '+ str(IPaddress_Lo) + '/32',
                                                'no shutd']
                        result_command_sent = ssh.send_config_set(command)
                        print(result_command_sent)
                        f.write(result_command_sent)
                        f.write("\n" )

        for vlan in vlans:
            print(vlan)


            command_dhcp_relay_src = ['interface ' + str(vlan),
                                                            'ip dhcp relay source-interface Lo10',
                                                            ]
            result_dhcp_relay_src_command_sent = ssh.send_config_set(command_dhcp_relay_src)
            print(result_dhcp_relay_src_command_sent)
            f.write(result_dhcp_relay_src_command_sent)
            f.write("\n" )
            command_dhcp_relay_src_check = [
                                                                            ' show run interface ' + str(vlan),
                                                                            ' show interface ' + str(vlan) +  ' brief' ,
                                                                        ]
            result_dhcp_relay_src_command_check = ssh.send_command(command_dhcp_relay_src_check)
            print(result_dhcp_relay_src_command_check)
            f.write(result_dhcp_relay_src_command_check)
            f.write("\n" )         

        ssh.send_command('copy r s')       
        print('saving configurtion')     
        f.write('saving configurtion')                
        f.write("\n" )  

#=================================================
#               Main :  Credentials/connecting to jump server
#=================================================

if __name__ == "__main__":

# Get current time in ISO format
    time_now= datetime.now().isoformat(timespec="seconds")

#=================================================
#             Run "max_workers" threads to connect to the devices
#=================================================

# Print time when script has started
    print('  Start_time:' + str(time_now))
    hosts =  list_hosts( "yml/leaf_work_VxLAN_" + DCname + ".yml")
    n9k_devices = hosts['n9khosts']

# Each element (dictionary) within
#     the list is passed to the map function for establishing asynchronous SSH sessions to each device. Each element
#     that is passed to the map function is then sent to the session_handler function. Threadpool count can be adjusted
#     to accommodate for more SSH sessions.

    with ThreadPoolExecutor(max_workers=6) as threads:
        future_list = []
        for device in n9k_devices:
            future = threads.submit(Login, device)
            future_list.append(future)

        # for f in as_completed(future_list):
        #     print(f.result())

# Print time when script started and finished
    print('Finish_time: ' + str(datetime.now().isoformat(timespec="seconds")) +'  Start_time:' + str(time_now))
