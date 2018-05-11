import socket
import sys
import time
import random
import json
from collections import OrderedDict
import math
import random


def craft(row, variable, value):

	payload = OrderedDict()
	data = OrderedDict()

	payload["header"] = OrderedDict()
	payload["header"]["urlExtension"] = ["scoreboard"]
	payload["header"]["device"] = "prog3"
	payload["header"]["event"] = variable + "_update"

	data["row"] = row
	data["column"] = variable
	data["value"] = value
	
	# a color scheme that might be used.
	if isinstance(value, basestring): color = "white"
	elif value == 10: color = "aqua"
	elif value >= 9: color = "green"
	elif value >= 8: color = "yellow"
	elif value >= 7: color = "orange"
	else: color = "red"
	data["color"] = color

	payload["data"] = data
	return payload


def client(ip, port, message):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ip, port))
	try:
		#print json.dumps(message)
		sock.sendall(json.dumps(message))
		response = sock.recv(1024)
		print "Received: {}".format(response)
	finally:
		sock.close()
		

while True:
	HOST, PORT = "localhost", 4545
	
	the_num = random.randint(1,3)
	
	#decide randomly which variable's value is being changed
	if the_num == 1:
		var = "x"
	elif the_num == 2:
		var = "y"
	elif the_num == 3:
		var = "z"
		
	new_val = random.randint(1, 10)
			
	current_payload = craft("Current Value", var, new_val)
	last_update_payload = craft("Last Update From", var, "prog3.py")
	client(HOST, PORT, current_payload)
	client(HOST, PORT, last_update_payload)

	time.sleep(2)
	print("end")
