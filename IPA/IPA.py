#!/usr/bin/env python3

import os
import IPAController
import IPAModel
import IPAView


class IPA:
	"""
	This is the main program class of IPA: Image Processing Application. 
	"""
	def __init__(self):
		self.model = IPAModel.IPAModel()
		self.controller = IPAController.IPAController(self.model)
		self.controller.start()

ipa = IPA()			# This call doesn't return until the application terminates