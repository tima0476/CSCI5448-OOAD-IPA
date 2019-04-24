class ImageVitals:
	"""
	class ImagesVitals is a simple data container with named attributes for storing vital information about an image.
	"""
	def __init__(self):
		self.origImage = None
		self.tkImage = None
		self.modTkImage = None
		self.imgCanvas = None
		self.origSize = (None,None)
		self.currZoom = None
		self.title = ""