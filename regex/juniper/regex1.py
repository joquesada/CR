import re

interface_map = {}

with open('re_file.txt','r') as f:
    contents = f.read()
    for line in contents.splitlines():
        interface = re.findall(r'([^\s]+)',line)
        int_list = interface
        if 'xe' in int_list[0] and len(int_list) > 4:
            desc_join = ' '.join(map(str, int_list[3:]))
            interface_map['interface'] = int_list[0]
            if int_list[1] == 'up':                
                interface_map['admin'] = int_list[1]
                interface_map['link'] = int_list[2]
                interface_map['description'] = desc_join

            elif int_list[1] == 'down':                
                interface_map['admin'] = int_list[1]
                interface_map['link'] = int_list[2]
                interface_map['description'] = desc_join            

            else:                
                desc_elem = ' '.join(map(str, int_list[1:]))
                interface_map['admin'] = 'Null'
                interface_map['link'] = 'Null'
                interface_map['description'] = desc_elem        

        elif 'xe' in int_list[0] and len(int_list) == 1:
            interface_map['interface'] = int_list[0]
            interface_map['admin'] = 'Null'
            interface_map['link'] = 'Null'
            interface_map['description'] = 'Null'
      
        print(interface_map)
