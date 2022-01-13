#!/usr/bin/env python3
import socket
import paramiko
import threading
import sys
import getpass
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
	def __init__(self):
		self.event = threading.Event()
	
	def check_request(self, kind, chanid):
		if kind == 'session':
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
		session.bind((ip, 22))
		session.listen(100)
		print ("[*] Listening for connection .....")
	except Exception as e:
		print ("")
		# interuppted by jahd :(
