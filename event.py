class Event:
	"""
		Represents an event. An event defines the type of update a device will send
		to the viztool hub and which data fields will be sent.
	"""

	def __init__(self, name):
		self.name = name
		self.graphs = {}
		self.token = ""

	def getName(self):
		return self.name

	def addGraph(self, graph_name, dataPoints):
		self.graphs[graph_name] = dataPoints

	def getGraphsAndPoints(self):
		return self.graphs

	def hasToken(self):
		if self.token:
			return True
		else:
			return False

	def getToken(self):
		return self.token
