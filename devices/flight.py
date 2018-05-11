import socket
import sys
import time
import random
import json
from collections import OrderedDict
import math

lat = 38.990895
lng = -76.942331

oriLat = 38.990895
oriLng = -76.942331

def generate(i):
    global lat, lng

    payload = OrderedDict()
    data = OrderedDict()

    payload["header"] = OrderedDict()
    payload["header"]["urlExtension"] = ["mapbox"]
    payload["header"]["device"] = "flight"
    payload["header"]["event"] = "new_spot"
    payload["header"]["token"] = ""

    data = OrderedDict()

    lat += float(format((random.random())/100, '.5f'))
    data["lat"] = lat

    lng += float(format((random.random())/100, '.5f'))
    data["lng"] = lng

    if (data["lat"] > 41 or data["lng"] > -74):
        lat = oriLat
        lng = oriLng
        
    payload["data"] = data
    print json.dumps(payload)
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

    for i in range(1):
        payload = generate(i)
        client(HOST, PORT, payload)


    time.sleep(3)
    print("end")
