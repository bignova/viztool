import requests
import json
import argparse
from collections import OrderedDict
import socket
import sys
import time
import math

def craft(color, message, week, team, token, table_token):

    payload = OrderedDict()
    data = OrderedDict()

    payload["header"] = OrderedDict()
    payload["header"]["urlExtension"] = ["status_page"]
    payload["header"]["device"] = "status_updater"
    payload["header"]["event"] = team + "_update"
    payload["header"]["token"] = token

    data["row"] = team
    data["column"] = week
    data["value"] = message
    data["color"] = color
    data["table_token"] = table_token

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
    HOST, PORT = "128.8.127.100", 4545

    valid_colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple']
    valid_teams = ['Viztool', 'Calendar', 'Collaboration', 'Decisions', 'Mimtool', 'Scrapbook']
    valid_weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6',
    'Week 7', 'Week 8', 'Week 9', 'Week 10', 'Week 11', 'Week 12']
    expectedToken = "CMSC435"

    team = ''
    week = ''
    color = ''
    token = ''
    table_token = ''

    while team not in valid_teams:
        print "Enter a valid Team from %s" % str(valid_teams)
        team = raw_input()

    while week not in valid_weeks:
        print "Enter a valid week from %s" % str(valid_weeks)
        week = raw_input()

    print "Enter a message"
    message = raw_input()

    while color.lower() not in valid_colors:
        print "Enter a valid color from %s" % str(valid_colors)
        color = raw_input()

    while (token != expectedToken):
        print "Enter the token required to update CMSC435 status"
        token = raw_input()

    print "Enter a the team specific table token your team was provided"
    table_token = raw_input()

    for i in range(1):
        payload = craft(color, message, week, team, token, table_token)
        client(HOST, PORT, payload)

    time.sleep(3)
    print("end")
