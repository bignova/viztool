import socket
import sys
import time
import random
import json
from collections import OrderedDict
import math



def generate(i):

    payload = OrderedDict()
    data = OrderedDict()

    round1 = ["HOU 4-1 MIN", "OKC 2-4 UTA", "POR 0-4 NOP", "GSW 4-1 SAS", "TOR 4-2 WAS",  "CLE 4-3 IND", "PHI 4-1 MIA", "BOS 4-3 IND"]
    round2 = ["HOU 4-1 UTA","NOP 1-4 GSW","TOR 0-4 CLE","PHI 4-3 BOS"]
    round3 = ["HOU 4-2 GSW", "PHI 4-3 CLE"]
    final = ["HOU 2-4 PHI"]

    payload["header"] = OrderedDict()
    payload["header"]["urlExtension"] = ["flow"]
    payload["header"]["device"] = "flowAddE"
    payload["header"]["event"] = "addE"
    payload["header"]["token"] = ""

    data = OrderedDict()

    if i < 8:
        data["operation"] = "addEdge"
        data["target"] = round1[i] + "->" + round2[i/2]
    elif i < 12:
        data["operation"] = "addEdge"
        data["target"] = round2[i-8] + "->" + round3[(i-8)/2]      
    else: 
        data["operation"] = "addEdge"
        data["target"] = round3[i-12] + "->" + final[0]   


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

    for i in range(14):
        payload = generate(i)
        #print(payload)
        client(HOST, PORT, payload)
        time.sleep(1)

    exit()



    print("end")
