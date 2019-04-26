from PIL import Image
from PIL.ImageTk import PhotoImage 
import PIL.ImageEnhance as pie
import ImageVitals

class IPAModel:
	"""
	class IPAModel implements the image manipulation logic for IPA.
	"""
	def __init__(self):
		"""
		Constructor creates empty lists for aggregation of the ImageVitals objects and the subscribed observers.
		"""
		self.images = []			# this list will hold instances of ImageVitals
		self.observers = []			# this list will hold object references for observers.  Objects in this
									# list must implement an UpdateImage(ImageVitals) method
		self.activeImage = None

	def addImage(self, imgInfo):
		"""
		Save an ImageVitals object in the images list

		Parameters:
			imgInfo: ImageVitals reference for the new image.
		"""
		self.images.append(imgInfo)

	def setActiveImage(self, idx):
		"""
		Select a different image to be active

		Paramters:
			idx: int zero-based index of the image to be activated.
		"""
		if (idx < len(self.images) and (idx>=0)):
			self.activeImage = idx
	
	def getActiveImageIdx(self):
		"""
		return the zero-based index of the active image.
		"""
		return self.activeImage

	def getActiveImageInfo(self):
		"""
		return a reference to the ImageVitals object for the currently active image.
		"""
		return self.images[self.getActiveImageIdx()]

	def zoomActiveImage(self, value):
		"""
		Update the resize amount for the currently active image.

		Parameters:
			value:  float - the new magnification multiplier.  1.0 = original size.
		"""
		self.getActiveImageInfo().currZoom = value
		self.applyAdjustments()

	def adjustActiveSaturation(self, value):
		"""
		Update the saturation amount for the currently active image.

		Paramters:
			value: float - the new saturation amount.  1.0 = no change from original image.
		"""
		self.getActiveImageInfo().currSaturation = value
		self.applyAdjustments()

	def adjustActiveContrast(self, value):
		"""
		Update the contrast amount for the currently active image.

		Paramters:
			value: float - the new contrast amount.  1.0 = no change from original image.
		"""
		self.getActiveImageInfo().currContrast = value
		self.applyAdjustments()

	def adjustActiveBrightness(self, value):
		"""
		Update the brightness amount for the currently active image.

		Paramters:
			value: float - the new brightness amount.  1.0 = no change from original image.
		"""
		self.getActiveImageInfo().currBrightness = value
		self.applyAdjustments()

	def applyAdjustments(self):
		"""
		Apply the current adjustement values to all adjustments
		"""
		ii = self.getActiveImageInfo()

		# Zoom
		newSize = ( int(ii.origSize[0]*ii.currZoom), int(ii.origSize[1]*ii.currZoom) )
		ii.modImage = ii.origImage.resize(size=newSize, resample=Image.LANCZOS)

		# Saturation
		enhancer = pie.Color(ii.modImage)
		ii.modImage = enhancer.enhance(ii.currSaturation)

		# Contrast
		enhancer = pie.Contrast(ii.modImage)
		ii.modImage = enhancer.enhance(ii.currContrast)

		# Brightness
		enhancer = pie.Brightness(ii.modImage)
		ii.modImage = enhancer.enhance(ii.currBrightness)

		# PLACEHOLDER: This is where we would iterate through "doit" calls to registered plugins.

		# Ready the final image for display
		ii.modTkImage = PhotoImage(image=ii.modImage)

		# Notify all of our subscribers that the active image has been updated.
		self.notifyObservers()

	def registerObserver(self, o):
		"""
		register an observer which will receive notifications whenever the active image is updated.

		Paramters:
			o:  Object reference.  The object referenced must implement the updateImage(ImageVitals) method
		"""
		self.observers.append(o)

	def notifyObservers(self):
		"""
		iterate through the registered observers and notify each that the active image has been updated.
		"""
		img = self.getActiveImageInfo()
		for o in self.observers:
			o.updateImage(img)


