import os
import IPAModel
import IPAView
import ImageVitals

class IPAController:
	def __init__(self, model):
		self.model = model
		self.view = IPAView.IPAView(self, self.model)

	def start(self):
		self.view.CreateUI()
		self.view.start()

	def openImage(self, filepath):
		"""
		Open an image file and add a tab to display it.
		"""

		# Tell the view to open the image, and start creating the ImageVitals record for the model
		imgInfo = ImageVitals.ImageVitals()
		(imgInfo.origImage, imgInfo.tkImage) = self.view.loadImage(filepath)
		imgInfo.modTkImage = imgInfo.tkImage		# in the beginning, the image is unmodified
		imgInfo.origSize = (imgInfo.tkImage.width(), imgInfo.tkImage.height())
		imgInfo.currZoom = 1.0			# Start at 100% zoom


		# Make the image persistent - save the ImageVitals structure in the model
		self.model.addImage(imgInfo)

		# Now have the view add a tab to the notebook, and display the image on that tab pane
		(_, imgInfo.title) = os.path.split(filepath)	# pull out the filenme to use as the tab title
		idx = self.view.addImageTab(imgInfo)
		self.model.setActiveImage(idx)

