#!/usr/bin/env python3
import socket
import paramiko
import threading
import sys
import getpass
#TODO: dynamicly get creds 
#TODO: implement client side of ssh

# e.g. /home/<username>/.ssh/id_rsa.pub
rsa_key = ""
#get credentials 
username = input("username : ")
password = getpass.getpass()
credentials = {
	"username": username,
	"password": password
}


key = paramiko.RSAKey(filename=rsa_key)

class Server (paramiko.ServerInterface):
	def __init__(self,username, password, kind , chanid, ip):
		self.event = threading.Event()
		self.run(self.username, self.password, self.kind , self.chanid, self.ip)
	
	def check_request(self, kind, chanid):
		if self.kind == 'session':
			return paramiko.OPEN_SUCCEEDED
		return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
	

	def check_credentials(self, username , password):
		if username == credentials["username"] and password == credentials["password"]:

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
			client , addr = sock.accept()
			print ("[+] Connection Established")
		except Exception, e:
			print ("[-] Connection failed: " + str(e))

	def trasport(self):
		client = self.listener.client
		t = paramiko.Trasport(client)		
		try:
			t.load_server_moduli()
		except:
			print("[-] failed to load moduli")
			raise
		t.add_server_key(key)
		server = Server()
		try:
			t.start_server(server=server)
		except paramiko.SSHExeption, x:
			print ("[-] SSH hadnshake failed")

		chan = t.accept(20)
		print ("[+] Authenticated")
		print (chan.recv(1024))
		chan.send('CMD TO SEND')

	except Exception, e:
		print ("[-] Error occured: " str(e.class) + ":" str(e))
	try:
		t.close()
	except:
		pass
		sys.exit(1)

	def run(self, username, password, kind , chanid, ip):
		self.check_request(self.kind, chanid)
		self.check_credentials(self.username,self.password)
		self.listener(self.ip)
		self.trasport()








