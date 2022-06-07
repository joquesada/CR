import re
import json

interface_map = {}

with open('re_file.txt','r') as f:
    
    contents = f.read()    
    for line in contents.splitlines():

        interface = re.findall(r'([^\s]+)',line)
        int_list = interface
        if len(int_list) > 2:

            interface_map['interface'] = int_list[0]
            interface_map['IP_address'] = int_list[1]
            interface_map['Status'] = int_list[2]
            dict_file = open('output','a')
            json.dump(interface_map,dict_file,indent=4)
            dict_file.close()
            print(interface_map)
