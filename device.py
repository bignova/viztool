class Device:
	"""
		Represents a device. A "device" is any physical device or
		program/script that sends data updates to the viztool hub for visualization.

		This object holds the name of the device, and a map of event name to event object
		for all events sent by the device.
	"""

	def __init__ (self, name):
		self.name = name

		#Map of event name to event object
		self.events = []

	def getName(self):
		return self.name

	def getEventObjectByName(self, eventName):
		for event in self.events:
			if event.getName() == eventName:
				return event

	def getEvents(self):
		return self.events

	def getListOfEventNames(self):
		listOfNames = []
		for event in self.events:
			listOfNames.append(event.getName())

		return listOfNames
