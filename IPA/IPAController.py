# This file implements the IPAController class, which is the "Creamy Controller" of the MVC pattern.
# author: Timothy Mason

import os
import IPAModel
import IPAView
import ImageVitals

class IPAController:
	"""
	class IPAController implements the "Creamy Controller" of the MVC pattern for IPA.  This is the
	glue logic for controlling the IPA application.
	"""
	def __init__(self, model):
		# Constructor saves a passed-in reference to the model, and instantiates a view
		self.model = model
		self.view = IPAView.IPAView(model, self)

	def start(self):
		# The the view to create the user interface and start the main event loop.  Note: this method
		# doesn't return to the caller until the application is exited.  All program logic after this
		# point must be implemented as callbacks.
		self.view.CreateUI()
		self.view.start()

	def openImage(self, filepath):
		"""
		Open an image file and add a tab to display it.
		Parameters:
			filepath:  String containing the fully qualified path of the imge file to open
		"""

		# Tell the view to open the image, and start creating the ImageVitals record for the model
		# TODO - move this to the model
		imgInfo = ImageVitals.ImageVitals()
		(imgInfo.origImage, imgInfo.tkImage) = self.view.loadImage(filepath)
		imgInfo.modImage = imgInfo.origImage		# in the beginning, the image is unmodified
		imgInfo.modTkImage = imgInfo.tkImage
		imgInfo.origSize = (imgInfo.tkImage.width(), imgInfo.tkImage.height())
		imgInfo.currZoom = 1.0			# Start at 100% zoom
		imgInfo.path = filepath

		# Save the ImageVitals
		self.model.addImage(imgInfo)

		# Now have the view add a tab to the notebook, and display the image on that tab pane
		(_, imgInfo.title) = os.path.split(filepath)	# pull out the filenme to use as the tab title
		idx = self.view.addImageTab(imgInfo)
		self.model.setActiveImage(idx)

		self.view.updateControls(imgInfo)	# Update all of the slider controls for the newly active image

	def activeImageChanged(self, idx):
		"""
		To be invoked by the view whenever the active image is changed (for example, by selecting
		a different tab in the notebook control)

		Parameters:
			idx = int index number of the newly active tab.
		"""
		self.model.setActiveImage(idx)
		self.view.updateControls(self.model.getActiveImageInfo())	# Update all of the slider controls for the newly active image

	def zoomImage(self, value):
		"""
		Change the zoom magnification of the current image.
		Parameters:
			value = float value of the desired magnification (1.0 is original size)
		"""
		self.model.zoomActiveImage(value)

	def adjustSaturation(self, value):
		"""
		Change the saturation of the current image.
		Parameters:
			value = float value for amount of adjustment based on original image (1.0 is no adjustment)
		"""
		self.model.adjustActiveSaturation(value)

	def adjustContrast(self, value):
		"""
		Change the contrast of the current image.
		Parameters:
			value = float value for amount of adjustment based on original image (1.0 is no adjustment)
		"""
		self.model.adjustActiveContrast(value)

	def adjustBrightness(self, value):
		"""
		Change the brightness of the current image.
		Parameters:
			value = float value for amount of adjustment based on original image (1.0 is no adjustment)
		"""
		self.model.adjustActiveBrightness(value)
