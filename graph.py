import numpy

class Graph:
	"""
		Represents a graph. A "graph" is any singular
		visualization on the front end.

		This object holds the name of the graph, the formatting json
		for the graph, and a list of lists holding the device, event,
		and data keys the graph depends upon
	"""

	def __init__ (self, name, json_str):
		self.name = name
		self.json_format = json_str

		#Map of event name to event object
		self.sources = {}

		self.dataArray = []



	def addSource(self, device, event, dataPoints):
		self.sources[device][event].append(datapoints)

	def getName(self):
		return self.name

	def getDataPointsByDeviceEvent(self, devName, eventName):
		return self.sources[devName][eventName]

	def getSources(self):
		return self.sources

	def getListOfDeviceNames(self):
		return self.sources.keys()

	def getFormat(self):
		return self.json_format

	def updateDataArray(self, messageStr):
		
		if len(self.dataArray) < 10:
			self.dataArray.append(messageStr)
		else:
			self.dataArray.pop(0)
			self.dataArray.append(messageStr)

	def getDataArray(self):
		return self.dataArray
