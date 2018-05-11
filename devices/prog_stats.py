import socket
import sys
import time
import random
import json
from collections import OrderedDict
import math
import random

stats = {
 "low_x": 11,
 "high_x": 0,
 "low_y": 11,
 "high_y": 0,
 "low_z": 11,
 "high_z": 0
}

def craft(row, variable, value):

	payload = OrderedDict()
	data = OrderedDict()

	payload["header"] = OrderedDict()
	payload["header"]["urlExtension"] = ["scoreboard_stats"]
	payload["header"]["device"] = "prog_stats"
	payload["header"]["event"] = variable + "_update"

	data["row"] = row
	data["column"] = variable
	data["value"] = value
	
	# a color scheme that might be used.
	if isinstance(value, basestring): color = "white"
	elif value == 10: color = "aqua"
	elif value >= 9: color = "lime"
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
		
def isLower(var, current_val):
	return  ((var == "x" and current_val < stats["low_x"]) or 
	(var == "y" and current_val < stats["low_y"]) or 
	(var == "z" and current_val < stats["low_z"]))
	
def isHigher(var, current_val):
	return ((var == "x" and current_val > stats["high_x"]) or 
	(var == "y" and current_val > stats["high_y"]) or 
	(var == "z" and current_val > stats["high_z"]))
		
def setLow(var, value):
	if var == "x":
		stats["low_x"] = value
	elif var == "y":
		stats["low_y"] = value
	elif var == "z":
		stats["low_z"] = value

def setHigh(var, value):
	if var == "x":
		stats["high_x"] = value
	elif var == "y":
		stats["high_y"] = value
	elif var == "z":
		stats["high_z"] = value
		
def getLow(var):
	if var == "x":
		return stats["low_x"]
	elif var == "y":
		return stats["low_y"]
	elif var == "z":
		return stats["low_z"]

def getHigh(var):
	if var == "x":
		return stats["high_x"]
	elif var == "y":
		return stats["high_y"]
	elif var == "z":
		return stats["high_z"]

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
		
	if isLower(var, new_val):
		setLow(var, new_val)
		low_payload = craft("Low", var, getLow(var))
		low_from_payload = craft("Low Seen From", var, "prog_stats.py")
		client(HOST, PORT, low_payload)
		client(HOST, PORT, low_from_payload)
	if isHigher(var, new_val):
		setHigh(var, new_val)
		high_payload = craft("High", var, getHigh(var))
		high_from_payload = craft("High Seen From", var, "prog_stats.py")
		client(HOST, PORT, high_payload)
		client(HOST, PORT, high_from_payload)
				
	current_payload = craft("Current Value", var, new_val)
	last_update_payload = craft("Last Update From", var, "prog_stats.py")
	client(HOST, PORT, current_payload)
	client(HOST, PORT, last_update_payload)

	time.sleep(.5)
	print("end")
