import requests
import json
import argparse
from collections import OrderedDict
import socket
import sys
import time
import math
from datetime import datetime
from bs4 import BeautifulSoup as bs

def parse(ticker):
    data = OrderedDict()
    url = "http://finance.yahoo.com/quote/%s?p=%s"%(ticker,ticker)
    r = requests.get(url, verify=False)
    print ("Parsing %s"%(url))
    price = 0.0
    volume = 0
    soup = bs(r.content, "html.parser")
    for s in soup.find_all('span'):
        if s.get('class') != None and ('Trsdu(0.3s)' in s.get('class')) and ('Fw(b)' in s.get('class') and 'Fz(36px)' in s.get('class') and 'Mb(-4px)' in s.get('class')):
            price = float(s.get_text().replace(',',''))
    
    for s in soup.find_all('td'):
        if s.get('class') != None and (s.get('data-test') == 'TD_VOLUME-value'):
            v = s.find('span')
            volume = float(v.get_text().replace(',',''))
            print(volume)

    data['price'] = price
    data['volume'] = volume
    return data

def getUTCStr():
    utcnow = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(utcnow)
    return utcnow

def craft():
    payload = OrderedDict()
    data = OrderedDict()

    payload["header"] = OrderedDict()
    payload["header"]["urlExtension"] = ["stocks"]
    payload["header"]["device"] = "scraper"
    payload["header"]["event"] = "stock_update"
    payload["header"]["token"] = "test"

    data["time"] = getUTCStr()

    amd_data = parse('AMD')
    snap_data = parse('SNAP')
    svxy_data = parse('SVXY')

    data["amd_price"] = amd_data['price']
    data["snap_price"] = snap_data['price']
    data["svxy_price"] = svxy_data['price']

    data["amd_volume"] = amd_data['volume']
    data["snap_volume"] = snap_data['volume']
    data["svxy_volume"] = svxy_data['volume']


    payload["data"] = data
    return payload


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        print(message)
        sock.sendall(json.dumps(message))
        response = sock.recv(1024)
        print "Received: {}".format(response)
    finally:
        sock.close()
while True:
    HOST, PORT = "localhost", 4545

    for i in range(1):
        payload = craft()


        client(HOST, PORT, payload)


    time.sleep(3)
    print("end")