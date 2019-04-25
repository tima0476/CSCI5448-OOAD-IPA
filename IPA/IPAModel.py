from PIL import Image
from PIL.ImageTk import PhotoImage 
import PIL.ImageEnhance as pie
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
		self.applyAdjustments()

	def adjustActiveSaturation(self, value):
		self.getActiveImageInfo().currSaturation = value
		self.applyAdjustments()

	def adjustActiveContrast(self, value):
		self.getActiveImageInfo().currContrast = value
		self.applyAdjustments()

	def adjustActiveBrightness(self, value):
		self.getActiveImageInfo().currBrightness = value
		self.applyAdjustments()

	def applyAdjustments(self):
		"""
		Apply the current adjustement values to all 4 adjustments (zoom, saturation, contrast, brightness)
		"""
		ii = self.getActiveImageInfo()

		# Zoom
		newSize = ( int(ii.origSize[0]*ii.currZoom), int(ii.origSize[1]*ii.currZoom) )
		img = ii.origImage.resize(size=newSize, resample=Image.LANCZOS)

		# Saturation
		enhancer = pie.Color(img)
		img = enhancer.enhance(ii.currSaturation)

		# Contrast
		enhancer = pie.Contrast(img)
		img = enhancer.enhance(ii.currContrast)

		# Brightness
		enhancer = pie.Brightness(img)
		ii.modTkImage = PhotoImage(image=enhancer.enhance(ii.currBrightness))

