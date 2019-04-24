import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image
from PIL.ImageTk import PhotoImage 
import ScrolledCanvas
import ImageVitals
import IPAController

class IPAView:
	"""
	Class IPAView:  The view portion of the IPA MVC implementation.  This class is responsible for presenting
	the tkInter-based user interface for the IPA application.
	"""

	def __init__(self, controller, model):
		# Constructor:  Save references to the M and C of the MVC
		self.model = model
		self.controller = controller

	def CreateUI(self):
		# Make all of the needed tkInter calls to bring up the main application window.

		self.mainFrame = ttk.Frame(parent=None)
		self.mainFrame.pack()
		self.mainFrame.master.title("IPA: Image Processing Application")
		
		#
		# Create the row of control buttons along the bottom of the window
		#
		self.bottomFrame = ttk.Frame(self.mainFrame)
		self.bottomFrame.pack(side=tk.BOTTOM, fill='x', expand='true', anchor='s')
		self.closeButton = ttk.Button(self.bottomFrame, text="Close", command=self.onCloseButtonPress)
		self.saveButton = ttk.Button(self.bottomFrame, text="Save...", command=self.onSaveButtonPress, state='disabled')
		self.openButton = ttk.Button(self.bottomFrame, text='Open...', command=self.onOpenButtonPress)

		# Buttons will be placed from right to left in the order they are packed.
		self.closeButton.pack(side=tk.RIGHT)
		self.saveButton.pack(side=tk.RIGHT)
		self.openButton.pack(side=tk.RIGHT)

		# Use the remaining space in the bottom frame for the zoom slider (tk calls a slider a "Scale")
		self.zoomScale = ttk.Scale(self.bottomFrame, command=self.onZoomMove, from_=5, to=200, value=100, orient=tk.HORIZONTAL)
		self.zoomScale.pack(side=tk.RIGHT, fill='x', expand='true')
		ttk.Label(self.bottomFrame, text='Zoom: ').pack(side=tk.LEFT)	# Add a label so the user knows what it is

		#
		# Add a panel on the right for the 'extras'
		#
		self.rightFrame = ttk.Frame(self.mainFrame)
		self.rightFrame.pack(side=tk.RIGHT, fill='y', expand=tk.TRUE, anchor=tk.E)

		# Add 4 sliders to the action panel - Brightness, Contrast, Saturation, Tint
		rightScaleLabelsFrame = ttk.Frame(self.rightFrame)
		rightScaleLabelsFrame.pack(side=tk.TOP)
		
		# Detour to add the sliders so we can query their width then come back and
		# right-size the label images
		rightScaleFrame = ttk.Frame(self.rightFrame)
		rightScaleFrame.pack(side=tk.TOP)
		self.tintScale = ttk.Scale(rightScaleFrame, command=self.dummy, from_=0, to=100, orient=tk.VERTICAL)
		self.saturationScale = ttk.Scale(rightScaleFrame, command=self.dummy, from_=0, to=100, orient=tk.VERTICAL)
		self.contrastScale = ttk.Scale(rightScaleFrame, command=self.dummy, from_=0, to=100, orient=tk.VERTICAL)
		self.brightnessScale = ttk.Scale(rightScaleFrame, command=self.dummy, from_=0, to=100, orient=tk.VERTICAL)
		self.tintScale.pack(side=tk.RIGHT)
		self.saturationScale.pack(side=tk.RIGHT)
		self.contrastScale.pack(side=tk.RIGHT)
		self.brightnessScale.pack(side=tk.RIGHT)

		self.tintScale.update()						# Necessary to call update prior to querying the width (thanks, StackOverflow!)
		sliderWidth = self.tintScale.winfo_width()	# safe to assume all sliders have equal width.

		# Hack alert!  Tkinter doesn't support rotated text in labels, so load
		# images of the rotated text and scale to fit the sliders
		tempImg = Image.open('rotTint.png')
		scale = float(sliderWidth)/float(tempImg.width)
		self.imgTintLabel = PhotoImage(image=tempImg.resize(size=(int(round(tempImg.width*scale)), int(round(tempImg.height*scale)))))

		tempImg = Image.open('rotSaturation.png')
		scale = float(sliderWidth)/float(tempImg.width)
		self.imgSaturationLabel = PhotoImage(image=tempImg.resize(size=(int(round(tempImg.width*scale)), int(round(tempImg.height*scale)))))

		tempImg = Image.open('rotContrast.png')
		scale = float(sliderWidth)/float(tempImg.width)
		self.imgContrastLabel = PhotoImage(image=tempImg.resize(size=(int(round(tempImg.width*scale)), int(round(tempImg.height*scale)))))

		tempImg = Image.open('rotBrightness.png')
		scale = float(sliderWidth)/float(tempImg.width)
		self.imgBrightnessLabel = PhotoImage(image=tempImg.resize(size=(int(round(tempImg.width*scale)), int(round(tempImg.height*scale)))))
		
		ttk.Label(rightScaleLabelsFrame, justify=tk.LEFT, image=self.imgTintLabel).pack(side=tk.RIGHT)
		ttk.Label(rightScaleLabelsFrame, justify=tk.LEFT, image=self.imgSaturationLabel).pack(side=tk.RIGHT)
		ttk.Label(rightScaleLabelsFrame, justify=tk.LEFT, image=self.imgContrastLabel).pack(side=tk.RIGHT)
		ttk.Label(rightScaleLabelsFrame, justify=tk.LEFT, image=self.imgBrightnessLabel).pack(side=tk.RIGHT)

			
		#
		# Use the remaining space on top & left for the notebook panel which shows the images
		#
		imgFrame = ttk.Frame(self.mainFrame)
		imgFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE, anchor='nw')

		# add a ttk::Notebook widget.  This is a 'tabbed' panel where the images will be displayed...one image per 'tab'
		self.nb = ttk.Notebook(imgFrame, padding=0)
		self.nb.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
		self.nb.bind("<<NotebookTabChanged>>", self.onTabChanged)	# IPA::onTabChanged will now be called whenever the selected tab changes.
		self.nb.enable_traversal()	# enable keyboard controls.  
			# From https://docs.python.org/2/library/ttk.html#ttk.Notebook ...
			# This will extend the bindings for the toplevel window containing the notebook as follows:
			#
			# * Control-Tab: selects the tab following the currently selected one.
			# * Shift-Control-Tab: selects the tab preceding the currently selected one.

	def onCloseButtonPress(self):
		"""
		Button handler:  Called when the Close button is pressed
		"""
		# To Do - offer to save all unsaved edits
		self.mainFrame.quit()

	def onSaveButtonPress(self):
		"""
		Button handler:  Called when the Save... button is pressed
		TODO:  Make me sing!
		"""
		return

	def onOpenButtonPress(self):
		"""
		Button handler:  Called when the Open... button is pressed
		"""
		# Display a file chooser
		filepath = filedialog.askopenfilename(title="Choose An Image to Open")

		# if the user chose a file and pressed "OK", then tell the controller
		if filepath:
			self.controller.openImage(filepath)

	def loadImage(self, filepath):
		pilImage = Image.open(filepath)
		tkImage = PhotoImage(image=pilImage)
		return (pilImage, tkImage)
		
	def addImageTab(self, imgInfo):
		"""
		Add a tab to the notebook widget and display the passed-in image on it.
		return: int index of the new tab
		"""
		frame = ttk.Frame(self.nb)
		self.nb.add(frame, text=imgInfo.title, sticky='nesw')
		imgInfo.imgCanvas = ScrolledCanvas.ScrolledCanvas(frame)
		self.updateCanvasImage(imgInfo)

		# Now we have at least one image open.  Enable the Save... button
		self.saveButton['state'] = 'normal'

		# Make the new tab active
		endIdx = self.nb.index("end") - 1
		self.nb.select(endIdx)

		# return the index of the new tab
		return endIdx

	def updateCanvasImage(self, imgInfo):
		"""
		Given an existing tkInter canvas object and a PIL.PhotoImage, replace the image in the canvas
		"""

		# compute a maximum size based on the display size, accounting for other UI elements
		screenW = self.mainFrame.winfo_screenwidth()-self.rightFrame.winfo_width()-10
		screenH = self.mainFrame.winfo_screenheight()-self.bottomFrame.winfo_height()-10

		width = imgInfo.modTkImage.width()
		height = imgInfo.modTkImage.height()

		# create the canvas object on which the image will be displayed
		imgInfo.imgCanvas.config(width=min(screenW, width), height=min(screenH, height))	# size of the image region on screen
		imgInfo.imgCanvas.config(scrollregion=(0, 0, width, height))						# virtual size of the image
		imgInfo.imgCanvas.create_image(0, 0, image=imgInfo.modTkImage, anchor=tk.NW)		# 0,0 is the relative coordinates of the image
		imgInfo.imgCanvas.pack(fill=tk.BOTH)

		# To Do:  Restructure this according to
		# https://stackoverflow.com/questions/19838972/how-to-update-an-image-on-a-canvas
		# (only call create_image on the first round, and itemconfig on subsequent
		# updates.  Need to persist the object returned from the first
		# create_image() call)


	def onZoomMove(self, value):
		"""
		Event handler - the Zoom slider has moved. Scale the image on the current tab accordingly.
		"""

		# Tell the controller to change the zoom of the active image
		self.controller.zoomImage(float(value) / 100.0)

	def zoomImage(self, imgInfo):
		# # Get the active tab #.  Abort if no tabs
		# try:
		# 	tabIdx = self.getCurrentTabID()
		# except:
		# 	return

		newSize = ( int(imgInfo.origSize[0]*imgInfo.currZoom), int(imgInfo.origSize[1]*imgInfo.currZoom) )

		imgInfo.modTkImage = PhotoImage(image=imgInfo.origImage.resize(size=newSize, resample=Image.LANCZOS))
		
		self.updateCanvasImage(imgInfo)
		

	def onTabChanged(self, event):
		"""
		Event handler - called whenever the main Notebook's active tab selection changes.
		"""
		self.controller.activeImageChanged(self.getCurrentTabID())

	def getCurrentTabID(self):
		"""
		Return the zero-based index of the currently selected tab in the main Notebook widget
		"""
		return self.nb.index( self.nb.select() )
	
	def updateControls(self, imgInfo):
		"""
		Update the positions of all the sliders to match the currently active image
		"""
		self.zoomScale.set(imgInfo.currZoom * 100)

	def dummy(self):
		return

	def start(self):
		self.mainFrame.mainloop()
