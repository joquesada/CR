import re

interface_map = {}
OUTPUT_FILE = 'output.csv'

with open(OUTPUT_FILE,'w') as f:
    f.write('Interface,IP_address,Status' + '\n')
   
with open('re_file.txt','r') as f:
    
    contents = f.read()    
    for line in contents.splitlines():

        interface = re.findall(r'([^\s]+)',line)
        int_list = interface
        if len(int_list) > 2:

            interface_map['interface'] = int_list[0]
            interface_map['IP_address'] = int_list[1]
            interface_map['Status'] = int_list[2]
            with open(OUTPUT_FILE,'a') as w:
                w.write(interface_map['interface'] + ',' + interface_map['IP_address'] + ',' + interface_map['Status'] + '\n')
            print(interface_map)
