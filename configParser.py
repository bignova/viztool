import jsonpickle
import json
import os
import hashlib

class configParser(object):
	"""
		Parses JSON file to return a Config object containing devices and events
	"""

	def parseJSONConfig(self, jsonString):
		return jsonpickle.decode(jsonString)

	def compareHashes(self, fileName, oldHash):

		path = os.getcwd() + "/config/"
		hash_md5 = hashlib.md5()

		with open(path+fileName, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hash_md5.update(chunk)
		return oldHash == hash_md5.hexdigest()

	def createHash(self, fileName):
		path = os.getcwd() + "/config/"
		hash_md5 = hashlib.md5()
		with open(path+fileName, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hash_md5.update(chunk)
		return hash_md5.hexdigest()
