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
		return images[self.getActiveImageIdx()]

	def zoomActiveImage(self, factor):
		self.images[self.getActiveImageIdx()].currZoom = factor
		return