#!/usr/bin/env python3

import os
from IPAController import IPAController
from IPAView import IPAView


imgdir = "/Users/tim/Google Drive/Spring 2019/csci5448/Project/github/CSCI5448-OOAD-IPA/test_images/"

class IPA:
	"""
	This is the main program class of IPA: Image Processing Application. 
	"""
	def __init__(self):
		self.controller = IPAController()
		self.view = IPAView(self.controller)

	def go(self):
		self.view.go()
		
	# def onCloseButtonPress(self):
	# 	"""
	# 	Button handler:  Called when the Close button is pressed
	# 	"""
	# 	# To Do - offer to save all unsaved edits
	# 	self.mainFrame.quit()

	# def onSaveButtonPress(self):
	# 	"""
	# 	Button handler:  Called when the Save... button is pressed
	# 	"""

	# def onOpenButtonPress(self):
	# 	"""
	# 	Button handler:  Called when the Open... button is pressed
	# 	"""
	# 	# Display a file chooser
	# 	filepath = filedialog.askopenfilename(initialdir = imgdir, title="Choose An Image to Open")

	# 	# Open the chosen file (if any)
	# 	if filepath:
	# 		self.openImage(filepath)

	# def openImage(self, filepath):
	# 	"""
	# 	Open an image file and add a tab to display it.
	# 	"""

	# 	# Open the image file using PIL and save a reference to the image object (aggregation)
	# 	pilImage = Image.open(filepath)
	# 	tkImage = PhotoImage(image=pilImage)
	# 	origDim = (tkImage.width(), tkImage.height())

	# 	# Save the image information
	# 	self.pilImages.append(pilImage)
	# 	self.tkImages.append(tkImage)
	# 	self.modTkImages.append(tkImage)
	# 	self.origSizes.append(origDim)
	# 	self.currZoom.append(100)		# default zoom is 100%

	# 	# Add a tab to the main frame's notebook object, and display the image on that tab pane
	# 	(_,filename) = os.path.split(filepath)	# pull out the filename to use as the tab title
	# 	frame = tk.Frame(self.nb)
	# 	self.nb.add(frame, text=filename, sticky='nesw')

	# 	canvas = ScrolledCanvas(frame)
	# 	self.imgCanvases.append(canvas)

	# 	self.updateCanvasImage(canvas, tkImage)

	# 	# Now we have at least one image open.  Enable the Save... button
	# 	self.saveButton['state'] = 'normal'

	# 	# Make the new tab active
	# 	endIdx = self.nb.index("end")
	# 	self.nb.select(endIdx-1)

	# def updateCanvasImage(self, canvas, newImage):
	# 	"""
	# 	Given an existing tkInter canvas object and a PIL.PhotoImage, replace the image in the canvas
	# 	"""

	# 	# compute a maximum size based on the display size, leaving some buffer for other UI elements
	# 	screenW = self.mainFrame.winfo_screenwidth()-40
	# 	screenH = self.mainFrame.winfo_screenheight()-150

	# 	width = newImage.width()
	# 	height = newImage.height()

	# 	# create the canvas object on which the image will be displayed
	# 	canvas.config(width=min(screenW, width), height=min(screenH, height))	# size of the image region on screen
	# 	canvas.config(scrollregion=(0, 0, width, height))						# virtual size of the image
	# 	canvas.create_image(0, 0, image=newImage, anchor=tk.NW)				 			# 0,0 is the relative coordinates of the image
	# 	canvas.pack(fill=tk.BOTH)

	# 	# To Do:  Restructure this according to
	# 	# https://stackoverflow.com/questions/19838972/how-to-update-an-image-on-a-canvas
	# 	# (only call create_image on the first round, and itemconfig on subsequent
	# 	# updates.  Need to persist the object returned from the first
	# 	# create_image() call)


	# def zoomImage(self, value):
	# 	# Get the active tab #.  Abort if no tabs
	# 	try:
	# 		tabIdx = self.getCurrentTabID()
	# 	except:
	# 		return

	# 	newSize = ( int(self.origSizes[tabIdx][0]*float(value)/100.0), int(self.origSizes[tabIdx][1]*float(value)/100.0) )

	# 	newImg = self.pilImages[tabIdx].resize(size=newSize, resample=Image.LANCZOS)
	# 	newTkImg = PhotoImage(image=newImg)
	# 	self.modTkImages[tabIdx] = newTkImg

	# 	self.updateCanvasImage(self.imgCanvases[tabIdx], newTkImg)

	# def onZoomMove(self, value):
	# 	"""
	# 	Event handler - the Zoom slider has moved. Scale the image on the current tab accordingly.
	# 	"""
	# 	# Get the active tab #.  Abort if no tabs
	# 	try:
	# 		tabIdx = self.getCurrentTabID()
	# 	except:
	# 		return

	# 	# remember the new zoom for this image
	# 	self.currZoom[tabIdx] = int(round(float(value)))

	# 	# scale the image
	# 	self.zoomImage(value)
		

	# def onTabChanged(self, event):
	# 	"""
	# 	Event handler - called whenever the main Notebook's active tab selection changes.
	# 	"""
	# 	tabIdx = self.getCurrentTabID()

	# 	# Update the zoom slider to the current zoom for this tab
	# 	self.zoomScale.set(self.currZoom[tabIdx])

	# def getCurrentTabID(self):
	# 	"""
	# 	Return the zero-based index of the currently selected tab in the main Notebook widget
	# 	"""
	# 	return self.nb.index( self.nb.select() )

ipa = IPA()
ipa.go()			# This call doesn't return until the application terminates