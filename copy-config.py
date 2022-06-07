#!/usr/bin/env python3

from datetime import datetime
import Exscript.util.file as euf
import Exscript.util.start as eus
import Exscript.util.match as eum

hosts = euf.get_hosts_from_file('hosts.txt')
accounts = euf.get_accounts_from_file('accounts.cfg')

dateTimeObj = datetime.now()
timeObj = dateTimeObj.now()
timeStr = timeObj.strftime("%b-%d-%Y-%H:%M:%S")



def dump_config(job, host, conn):
    conn.execute('term len 0')
    conn.execute('show run')
    #get the hostname of the device
    hostname = eum.first_match(conn, r'^hostname\s(.+)$')
    cfg_file = 'configs/' + timeStr + '-' + hostname.strip() + '.cfg'
    config = conn.response.splitlines()
    #format cleanup
    for i in range(2):
        config.pop(i)
    config.pop(-0)
    config.pop(-1)
    #write config to file
    with open(cfg_file, 'w') as f:
        for line in config:
            f.write(line + '\n')

eus.start(accounts, hosts, dump_config, max_threads=2)
