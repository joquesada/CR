import paramiko
import time

print('creating ssh client')
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print('Connecting to the device')

switch1 = {'hostname':'n9k01-spine-eat1.vmware.com','username':'jquesada','password':'Cowintapate23'}

ssh_client.connect(**switch1)

shell = ssh_client.invoke_shell()
shell.send('ter len 0\n')
shell.send('sh version\n')
time.sleep(2)

output = shell.recv(10000)

output = output.decode('utf-8')
print(output)

print('closing connection')
if ssh_client.get_transport().is_active():
    ssh_client.close()
