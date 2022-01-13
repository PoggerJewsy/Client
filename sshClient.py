#!/usr/bin/env python3
import paramiko
import threading
ip = "127.0.0.1"
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(ip, username='root', password='PASSWORD')
chan = client.get_transport().open_session()
chan.send("[+] Connection Established")

print (chan.recv(1024))

client.close()
