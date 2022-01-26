#!/usr/bin/env python3
import requests
import re

status = requests.get('https://poggerpussy.github.io').text


with open("status","w+") as f:
	regex = re.sub(r"<.*?>",'', status)
	print (regex)
	f.write(regex)
    
