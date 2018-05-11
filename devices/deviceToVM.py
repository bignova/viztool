import socket
import sys
import time
import random
import json
from collections import OrderedDict
import math

def generate(i):
    ts = str(math.floor(time.time()))
    #ts = time.strftime("%H:%M:%S", time.localtime())
    val = format((random.random())*20 + 70, '.2f')

    payload = OrderedDict()
    data = OrderedDict()

    payload["header"] = OrderedDict()

    payload["header"]["urlExtension"] = ["temperature"]
    payload["header"]["device"] = "thermostat2"
    payload["header"]["event"] = "new_temperature"
    payload["header"]["token"] = "password"

    data = OrderedDict()
    data["time"] = ts
    data["temperature1"] = val

    val = format((random.random())*20 + 75, '.2f')
    data["temperature2"] = val

    val = format((random.random())*20 + 60, '.2f')
    data["temperature3"] = val

    val = format((random.random())*40 + 70, '.2f')
    data["temperature4"] = val

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
    HOST, PORT = "128.8.127.100", 4545

    for i in range(1):
        payload = generate(i)
        #print(payload)
        client(HOST, PORT, payload)


    time.sleep(3)
    print("end")
