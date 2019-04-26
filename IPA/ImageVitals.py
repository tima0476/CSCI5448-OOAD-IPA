# This file implements the ImageVitals class, which contains vital information to be stored about a single image.
# author: Timothy Mason

class ImageVitals:
	"""
	class ImagesVitals is a simple data container with named attributes for storing vital information about an image.
	"""
	def __init__(self):
		self.origImage = None			# the unmodified Pillow image object (as read from disk)
		self.modImage = None			# current Pillow image which will be displayed (may be edited)
		self.tkImage = None				# the Tkinter::Canvas compatible version of origImage
		self.modTkImage = None			# the Tkinter::Canvas compatible version of modImage
		self.imgCanvas = None			# the Tkinter Canvas object on which the image is displayed
		self.origSize = (None,None)		# (width, height) of the original image, stored as a 2-tuple of ints
		self.currZoom = 1.0				# (float) for the resize multiplier of the image.  1.0 is original size
		self.currSaturation = 1.0		# (float) for the Saturation modifier of the image.  1.0 is unmodified.
		self.currContrast = 1.0			# (float) for the Contrast modifier of the image.  1.0 is unmodified.
		self.currBrightness = 1.0		# (float) for the Brightness modifier of the image.  1.0 is unmodified.
		self.title = ""					# (string) the title string shown by the view for this image
		self.path = ""					# (string) the fully qualified os path of the image file.