#!/usr/bin/env python3
import socket
import paramiko
import threading
import sys
import getpass





#TODO: add custom commands


#TODO: dynamicly get creds idea : encoders         


#TODO: implement client side of ssh


# e.g. /home/<username>/.ssh/id_rsa


rsa_key = "private rsa key e.g /home/user/.ssh/id_rsa"
#get credentials 
username = "root"
# password = getpass.getpass()
password = "PASSWORD"


key = paramiko.RSAKey(filename=rsa_key)

class Server (paramiko.ServerInterface):
	def __init__(self, ip):
		self.event = threading.Event()
		self.username = username
		self.password = password
		self.ip = ip
		self.credentials = {
			"username": username,
			"password": password
		}
	
	def check_request(self, kind, chanid):
		if self.kind == 'session':
			return paramiko.OPEN_SUCCEEDED
		return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
	

	def check_credentials(self, username , password):
		if self.username == self.credentials["username"] and self.password == self.credentials["password"]:

			return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED

	def listener(self, ip):
		""" starting a listener """
		try:
			session = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			session.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
			session.bind((self.ip, 22))
			session.listen(100)
			print ("[*] Listening for connection .....")
			client , addr = session.accept()
			print ("[+] Connection Established")
		except Exception as e:
			print ("[-] Connection failed: " + str(e))

	def trasport(self):
		try:
			client = self.listener.client
			t = paramiko.Trasport(client)		
			try:
				t.load_server_moduli()
			except:
				print("[-] failed to load moduli")
				raise Exception
			t.add_server_key(key)
			server = Server()
			try:
				t.start_server(server=server)
			except paramiko.SSHExeption as  x:
				print ("[-] SSH hadnshake failed" + str(x))

			chan = t.accept(20)
			print ("[+] Authenticated")
			print (chan.recv(1024))
			chan.send('ifconfig')

		except Exception as e:
			print ("[-] Error occured: " + str(e))
		try:
			t.close()
		except:
			pass
			sys.exit(1)

	def run(self):
		self.check_credentials(self.username,self.password)
		self.listener(self.ip)
		self.trasport()







if __name__ == "__main__":
    server = Server("127.0.0.1")
    server.run()
