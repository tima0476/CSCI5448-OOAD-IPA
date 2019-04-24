import ImageVitals

class IPAModel:

	def __init__(self):
		self.images = []		# this list will hold instances of ImageVitals
		self.activeImage = None
		return

	def addImage(self, imgInfo):
		# Expects imgInfo is an ImageVitals object
		self.images.append(imgInfo)
		return

	def setActiveImage(self, n):
		if (n < len(self.images) and (n>=0)):
			self.activeImage = n
		return
	
	def getActiveImageIdx(self):
		return self.activeImage

	def getActiveImageInfo(self):
		return self.images[self.getActiveImageIdx()]

	def zoomActiveImage(self, value):
		self.getActiveImageInfo().currZoom = value

	def adjustActiveSaturation(self, value):
		self.getActiveImageInfo().currSaturation = value

	def adjustActiveContrast(self, value):
		self.getActiveImageInfo().currContrast = value

	def adjustActiveBrightness(self, value):
		self.getActiveImageInfo().currBrightness = value
