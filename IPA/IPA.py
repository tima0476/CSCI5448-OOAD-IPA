import os
import IPAController
import IPAModel

class IPA:
	"""
	This is the main program class of IPA: Image Processing Application. 
	"""
	def __init__(self):
		self.model = IPAModel.IPAModel()
		self.controller = IPAController.IPAController(self.model)
		self.controller.start()

if __name__ == '__main__':
	IPA()			# This call doesn't return until the application terminates