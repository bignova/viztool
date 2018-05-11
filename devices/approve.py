import socket
import sys
import time
import random
import json
from collections import OrderedDict
import math



def generate(i):

    val = (random.random())*(100-1)+1
    val2 = 100-val

    val = format(val)
    val2 = format(val2)

    payload = OrderedDict()
    data = OrderedDict()

    payload["header"] = OrderedDict()
    payload["header"]["urlExtension"] = ["approvalRate"]
    payload["header"]["device"] = "approve1"
    payload["header"]["event"] = "approvalRate1"
    payload["header"]["token"] = ""

    data = OrderedDict()
    data["approve"] = val
    data["disapprove"] = val2

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
        #print(payload)
        client(HOST, PORT, payload)


    time.sleep(3)
    print("end")
