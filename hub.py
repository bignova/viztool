import sys
import os
import socket
import threading
import SocketServer
import Queue
import time
import json
from collections import OrderedDict

import socketio
import eventlet
from flask import Flask, render_template

from configValidator import configValidator
from configParser import configParser
from config import Config
from device import Device
from event import Event

# make thread compatible with eventlet
eventlet.monkey_patch()
sio = socketio.Server()

app = Flask(__name__)

validator = configValidator()
parser = configParser()
dataQueue = Queue.Queue()

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		data = self.request.recv(1024)
		dataQueue.put(data)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

class Hub:
	def __init__(self, numProcessors, host, port):
		# Map of config file name to config objects
		self.configs = {}
		self.configHashes = {}

		self.server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
		self.server_thread = threading.Thread(target=self.server.serve_forever)
		self.server_thread.daemon = True
		self.server_thread.start()

		# create a thread pool of data processing handler
		self.processorThreads = []
		for i in range(numProcessors):
			self.processorThreads += [threading.Thread(target=self.processor)]

		for p in self.processorThreads:
			p.daemon = True
			p.start()

	def addConfig(self, name, config):
		self.configs[name] = config

	def getConfigs(self):
		return self.configs

	def addHash(self, name, hash):
		self.configHashes[name] = hash

	def getHashes(self):
		return self.configHashes

	def kill_server(self):
		self.server.shutdown()
		self.server.server_close()

	# thread that handles incoming data updates
	def processor(self):
		global dataQueue
		while True:
			data_update = json.loads(dataQueue.get().decode("utf-8"))

			if isValidStructure(data_update):
				header = data_update["header"]
				if isValidHeaderFormat(header):
					urlExtensionList = getUpdatedUrlExtensionList(header["urlExtension"])

					for url in urlExtensionList:
						config = hub.configs[url]
						deviceName = header["device"]
						if not deviceRegisteredInConfig(deviceName, config, url):
							continue
						else:
							device = config.getDeviceObjectByName(deviceName)
							eventName = header["event"]
							if not deviceContainsEvent(eventName, device):
								continue
							else:
								event = device.getEventObjectByName(eventName)
								if event.hasToken():
									if not verifyToken(header, event):
										continue

								graphs = config.getGraphsForDeviceEvent(deviceName, eventName)
								updateDataStoreAndForward(data_update["data"], graphs, config, url)


################## start helper functions for processor ##################

# checks that data updata contains a header section and data section
def isValidStructure(data_update):
	try:
		header = data_update["header"]
	except KeyError:
		reportError("Error: Data update is missing a 'header' section")
		return False

	try:
		data = data_update["data"]
	except KeyError:
		reportError("Error: Data update is missing a 'data' section")
		return False

	return True

# checks that the header contains all of the expected fields
def isValidHeaderFormat(header):
	try:
		urlExtensionList = header["urlExtension"]
	except KeyError:
		reportError("Error: Header of data update is missing an 'urlExtension' field")
		return False

	try:
		deviceName = header["device"]
	except KeyError:
		reportError("Error: Header of data update is missing a 'device' field")
		return False

	try:
		eventName = header["event"]
	except KeyError:
		reportError("Error: Header of data update is missing an 'event' field")
		return False

	return True

# removes urls/configs that have not yet been submitted to the hub
def getUpdatedUrlExtensionList(urlExtensionList):
	for url in urlExtensionList:
		if not url in hub.getConfigs():
			reportError("Error: config: %s not registered yet" % url)
			urlExtensionList.remove(url)

	return urlExtensionList

#returns true if deviceName is a device in the config file with urlExtension url
def deviceRegisteredInConfig(deviceName, config, url):
	if not deviceName in config.getListOfDeviceNames() :
		reportError("Error: device: " + deviceName + " not found in config with urlExtension: " + url)
		return False
	else:
		return True

# returns true if eventName is an event of device in the config file
def deviceContainsEvent(eventName, device):
	if not eventName in device.getListOfEventNames() :
		reportError("Error: event: " + eventName + " not found in device: " +  device.getName())
		return False
	else:
		return True

# returns True if the token of the data update matches that which was defined
# for the event in the config file
def verifyToken(header, event):
	try:
		token = header["token"]
	except KeyError:
		reportError("Error: Token expected for event: " + event.getName() + " but header of data update is missing a 'token' field")
		return False

	if not (token == event.getToken()):
		reportError("Error: Event token for event: " + event.getName() + " does not match")
		return False
	else:
		return True

# updates data store and forwards data updates to frontend
def updateDataStoreAndForward(data, graphs, config, urlExtension):
	for graph, datafields in graphs.items():
		if not containsAllExpectedDataFields(data, datafields, graph):
			continue
		else:
			payload = constructPayload(graph, datafields, data)

			#save data in graph object stored in the config
			graphObj = config.getGraphObjectByName(graph)
			graphObj.updateDataArray(json.dumps(payload))

			# forward data to frontend
			sio.emit('load', data=json.dumps(payload), room=urlExtension)


# checks that the data section contains all of the data fields that are defined
# in the data fields section under event in the config file
def containsAllExpectedDataFields(data, expectedDataFields, graph):
	for expectedField in expectedDataFields:
		try:
			value = data[expectedField]
		except KeyError:
			reportError("Error: failed to update graph " + graph + "; expected data section of update to contain data field named: " + expectedField)
			return False

	return True

# constructs the message that is to be sent to frontend and also stored
def constructPayload(graph, datafields, data):
	payload = OrderedDict()
	data_to_forward = OrderedDict()

	payload['graph_name'] = graph
	for field in datafields:
		data_to_forward[field] = data[field]
	payload['data'] = data_to_forward

	return payload

def reportError(errorMsg):
	sio.emit("error", data=json.dumps(errorMsg))

################## end helper functions for processor ##################

# parse the file and return a config instance, which contains all the devices, events and graphs
def initializer(hub, fileName):
	file = open(path + fileName, 'r')
	try:
		datastore = json.load(file)
	except:
		print("Error: invalid json for file %s" % fileName)
		return

	jsonString = json.dumps(datastore)
	
	if validator.isValidConfig(datastore):
		config = parser.parseJSONConfig(jsonString)
		config.storeGraphsInEvents()
		hub.addConfig(config.urlExtension, config)
		hub.addHash(config.urlExtension, parser.createHash(config.urlExtension+'.json'))


def serve_app(_sio, _app):
	# wrap Flask application with socketio's middleware
	app = socketio.Middleware(_sio, _app)

	# deploy as an eventlet WSGI server
	eventlet.wsgi.server(eventlet.listen(('', 8000)), app)

@app.route('/<config_name>')
def index(config_name):
	if config_name in hub.getConfigs().keys():
		return render_template('index.html', config=config_name)
	else:
		config_file = config_name + ".json"
		if (os.path.exists(path + config_file)):
			print("Initializing...")
			initializer(hub, config_file)
			print("\tNow serving: ")
			for c in hub.getConfigs().keys():
				print("\t%s" % c)
			return render_template('index.html', config=config_name)
		else:
			print("Error: config file does not exist")
			print("\tNow serving: ")
			for c in hub.getConfigs().keys():
				print("\t%s" % c)
			return render_template('config_missing.html', config=config_name, servingConfigs=json.dumps(hub.getConfigs().keys()))

# create a new socketio room for the current urlExtension
@sio.on('enter room')
def enter_room(sid, urlExtension):
	sio.enter_room(sid, urlExtension)

# remove the socketio room
@sio.on('leave room')
def leave_room(sid, urlExtension):
	sio.leave_room(sid, urlExtension)

@sio.on('ready')
def graph_initializer(sid, urlExtension): # data = url
	try:
		config = hub.getConfigs()[urlExtension]
		hash_ = hub.getHashes()[urlExtension]
	except KeyError:
		return

	if not parser.compareHashes(config.urlExtension+'.json', hash_):
		initializer(hub, config.urlExtension + '.json')

	sio.emit('generate', data=config.getListOfGraphJSONRepresentations(), room=urlExtension)

	for graph in config.getGraphs():
		for data in graph.getDataArray():
			sio.emit('load', data=data, room=urlExtension)

if __name__ == "__main__":
	HOST, PORT = "localhost", 4545

	global hub
	hub = Hub(4, HOST, PORT)

	path = os.getcwd() + "/config/"

	try:
		# run flask server
		serve_app(sio, app)
	finally:
		hub.kill_server()
		print("exit")
