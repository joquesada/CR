

from netmiko import ConnectHandler
import re
import Exscript.util.file as euf

hosts = euf.get_hosts_from_file('hosts.txt')
accounts = euf.get_accounts_from_file('accounts.cfg')

def get_hostname(dev):
#    dev.enable()
    hostname = dev.send_command("show run | i hostname").split()[1]
    print("Device: " + hostname)


def get_version(dev):
#    dev.enable()
    hostname = dev.send_command("show run | i hostname").split()[1]
    output = dev.send_command("show version")
    pattern = re.compile(r"Software, Version (\S+)")
    version_match = pattern.search(output)
    print("Software version: " + version_match.group(1))


for device in hosts:
    print("####################")
    get_hostname(device)
    print("####################")
    get_version(device)
    print("\n")
    device.disconnect()
