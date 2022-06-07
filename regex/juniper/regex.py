import re

interface_map = {}

with open('re_file.txt','r') as f:
    contents = f.read()
    for line in contents.splitlines():
        interface = re.findall(r'([^\s]+)',line)
        int_list = interface
        if len(int_list) > 4:
            desc_join = ' '.join(map(str, int_list[3:]))
            interface_map['interface'] = int_list[0]
            interface_map['admin'] = int_list[1]
            interface_map['link'] = int_list[2]
            interface_map['description'] = desc_join
            print(interface_map)
