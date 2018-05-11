class Config:
	"""
		Python object representing the config file.

		Contains a map of deviceName to device object.
		Each device object in turn contains map of events which
		hold the data fields and their types.
	"""
	def __init__(self, urlExtension):
		self.urlExtension = urlExtension
		self.devices = []
		self.graphs = []


	def getDeviceObjectByName(self, deviceName):
		for device in self.devices:
			if device.getName() == deviceName:
				return device

	def getDevices(self):
		return self.devices

	def getListOfDeviceNames(self):
		listOfNames = []
		for device in self.devices:
			listOfNames.append(device.getName())

		return listOfNames

	def addGraph(self, graph):
		self.graphs[graph.getName()] = graph

	def getGraphObjectByName(self, graphName):
		for graph in self.graphs:
			if graph.getName() == graphName:
				return graph

	def getGraphs(self):
		return self.graphs

	def getGraphsForDeviceEvent(self, deviceName, eventName):
		device = self.getDeviceObjectByName(deviceName)
		event = device.getEventObjectByName(eventName)
		return event.getGraphsAndPoints()

	def storeGraphsInEvents(self):
		for graph in self.graphs:
			s = graph.getSources()
			for deviceName in s:
				eventNames = s[deviceName]
				for eventName in eventNames:
					self.storeGraph(deviceName, eventName, graph.getName(), graph.getDataPointsByDeviceEvent(deviceName, eventName))

	def storeGraph(self, deviceName, eventName, graphName, graphPoints):
		device = self.getDeviceObjectByName(deviceName)
		try:
			event = device.getEventObjectByName(eventName)
		except:
			print ("Error: check that device name in 'sources' field of graph matches event name defined in device object")
		try:
			event.addGraph(graphName, graphPoints)
		except:
			print ("Error: check that event name in 'sources' field of graph matches event name defined in event object of device")

	def getListOfGraphJSONRepresentations(self):
		return [x.getFormat() for x in self.graphs]
