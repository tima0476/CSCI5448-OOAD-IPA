#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image
from PIL.ImageTk import PhotoImage 
from ScrolledCanvas import ScrolledCanvas

imgdir = "/Users/tim/Google Drive/Spring 2019/csci5448/Project/github/CSCI5448-OOAD-IPA/test_images/"

class IPA:
	"""
	This is the main program class of IPA: Image Processing Application. 
	"""
	def __init__(self):
		# Initialize persistent storage lists for images.  To Do - Code Smell...Make
		# an object storing all info about an object (MVC?)
		self.pilImages = []		# store PIL image objects
		self.tkImages = []		# store original tkInter PhotoImage objects
		self.modTkImages = []	# store interim PhotoImage objects
		self.imgCanvases = []	# store tkInter canvas objects (to enable changing the displayed image)
		self.origSizes = []		# store (w,h) tuples with the original dimensions of each image
		self.currZoom = []		# store the current zoom level for each image

		# To Do:  Move all of the UI creation / layout to a separate functions. 
		# Just layout the panels here, then "fill them in" with sub functions
		self.mainFrame = ttk.Frame(parent=None)
		self.mainFrame.pack()
		self.mainFrame.master.title("IPA: Image Processing Application")
		
		#
		# Create the row of control buttons along the bottom of the window in order from right to left
		#
		bottomFrame = ttk.Frame(self.mainFrame)
		bottomFrame.pack(side=tk.BOTTOM, fill='x', expand='true', anchor='s')
		self.closeButton = ttk.Button(bottomFrame, text="Close", command=self.onCloseButtonPress)
		self.saveButton = ttk.Button(bottomFrame, text="Save...", command=self.onSaveButtonPress, state='disabled')
		self.openButton = ttk.Button(bottomFrame, text='Open...', command=self.onOpenButtonPress)
		# Buttons will be placed from right to left in the order they are packed.
		self.closeButton.pack(side=tk.RIGHT)
		self.saveButton.pack(side=tk.RIGHT)
		self.openButton.pack(side=tk.RIGHT)

		# Use the remaining space in the bottom frame for the zoom slider (tk calls a slider a "Scale")
		self.zoomScale = ttk.Scale(bottomFrame, command=self.onZoomMove, from_=5, to=200, value=100, orient=tk.HORIZONTAL)
		self.zoomScale.pack(side=tk.RIGHT, fill='x', expand='true')
		ttk.Label(bottomFrame, text='Zoom: ').pack(side=tk.LEFT)	# Add a label so the user knows what it is

		#
		# Add a panel on the right for the 'extras'
		#
		rightFrame = ttk.Frame(self.mainFrame)
		rightFrame.pack(side=tk.RIGHT, fill='y', expand=tk.TRUE, anchor=tk.E)

		# Add 4 sliders to the action panel - Brightness, Contrast, Saturation, Tint
		rightScaleLabelsFrame = ttk.Frame(rightFrame)
		rightScaleLabelsFrame.pack(side=tk.TOP)
		
		# Detour to add the sliders so we can query their width then come back and
		# right-size the label images
		rightScaleFrame = ttk.Frame(rightFrame)
		rightScaleFrame.pack(side=tk.TOP)
		self.tintScale = ttk.Scale(rightScaleFrame, command=self.dummy, from_=0, to=100, orient=tk.VERTICAL)
		self.saturationScale = ttk.Scale(rightScaleFrame, command=self.dummy, from_=0, to=100, orient=tk.VERTICAL)
		self.contrastScale = ttk.Scale(rightScaleFrame, command=self.dummy, from_=0, to=100, orient=tk.VERTICAL)
		self.brightnessScale = ttk.Scale(rightScaleFrame, command=self.dummy, from_=0, to=100, orient=tk.VERTICAL)
		self.tintScale.pack(side=tk.RIGHT)
		self.saturationScale.pack(side=tk.RIGHT)
		self.contrastScale.pack(side=tk.RIGHT)
		self.brightnessScale.pack(side=tk.RIGHT)

		self.tintScale.update()
		sliderWidth = self.tintScale.winfo_width()	# safe to assume all sliders have equal width
		print("Slider width",sliderWidth)

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

	def dummy(self, value):
		print("dumdum")

	def go(self):
		"""
		Start the application running by firing off the tkInter event loop 
		"""
		self.mainFrame.mainloop()

	def onCloseButtonPress(self):
		"""
		Button handler:  Called when the Close button is pressed
		"""
		# To Do - offer to save all unsaved edits
		self.mainFrame.quit()

	def onSaveButtonPress(self):
		"""
		Button handler:  Called when the Save... button is pressed
		"""

	def onOpenButtonPress(self):
		"""
		Button handler:  Called when the Open... button is pressed
		"""
		# Display a file chooser
		filepath = filedialog.askopenfilename(initialdir = imgdir, title="Choose An Image to Open")

		# Open the chosen file (if any)
		if filepath:
			self.openImage(filepath)

	def openImage(self, filepath):
		"""
		Open an image file and add a tab to display it.
		"""

		# Open the image file using PIL and save a reference to the image object (aggregation)
		pilImage = Image.open(filepath)
		tkImage = PhotoImage(image=pilImage)
		origDim = (tkImage.width(), tkImage.height())

		# Save the image information
		self.pilImages.append(pilImage)
		self.tkImages.append(tkImage)
		self.modTkImages.append(tkImage)
		self.origSizes.append(origDim)
		self.currZoom.append(100)		# default zoom is 100%

		# Add a tab to the main frame's notebook object, and display the image on that tab pane
		(_,filename) = os.path.split(filepath)	# pull out the filename to use as the tab title
		frame = tk.Frame(self.nb)
		self.nb.add(frame, text=filename, sticky='nesw')

		canvas = ScrolledCanvas(frame)
		self.imgCanvases.append(canvas)

		self.updateCanvasImage(canvas, tkImage)

		# Now we have at least one image open.  Enable the Save... button
		self.saveButton['state'] = 'normal'

		# Make the new tab active
		endIdx = self.nb.index("end")
		self.nb.select(endIdx-1)

	def updateCanvasImage(self, canvas, newImage):
		"""
		Given an existing tkInter canvas object and a PIL.PhotoImage, replace the image in the canvas
		"""

		# compute a maximum size based on the display size, leaving some buffer for other UI elements
		screenW = self.mainFrame.winfo_screenwidth()-40
		screenH = self.mainFrame.winfo_screenheight()-150

		width = newImage.width()
		height = newImage.height()

		# create the canvas object on which the image will be displayed
		canvas.config(width=min(screenW, width), height=min(screenH, height))	# size of the image region on screen
		canvas.config(scrollregion=(0, 0, width, height))						# virtual size of the image
		canvas.create_image(0, 0, image=newImage, anchor=tk.NW)				 			# 0,0 is the relative coordinates of the image
		canvas.pack(fill=tk.BOTH)

		# To Do:  Restructure this according to
		# https://stackoverflow.com/questions/19838972/how-to-update-an-image-on-a-canvas
		# (only call create_image on the first round, and itemconfig on subsequent
		# updates.  Need to persist the object returned from the first
		# create_image() call)


	def zoomImage(self, value):
		# Get the active tab #.  Abort if no tabs
		try:
			tabIdx = self.getCurrentTabID()
		except:
			return

		newSize = ( int(self.origSizes[tabIdx][0]*float(value)/100.0), int(self.origSizes[tabIdx][1]*float(value)/100.0) )

		newImg = self.pilImages[tabIdx].resize(size=newSize, resample=Image.LANCZOS)
		newTkImg = PhotoImage(image=newImg)
		self.modTkImages[tabIdx] = newTkImg

		self.updateCanvasImage(self.imgCanvases[tabIdx], newTkImg)

	def onZoomMove(self, value):
		"""
		Event handler - the Zoom slider has moved. Scale the image on the current tab accordingly.
		"""
		# Get the active tab #.  Abort if no tabs
		try:
			tabIdx = self.getCurrentTabID()
		except:
			return

		# remember the new zoom for this image
		self.currZoom[tabIdx] = int(round(float(value)))

		# scale the image
		self.zoomImage(value)
		

	def onTabChanged(self, event):
		"""
		Event handler - called whenever the main Notebook's active tab selection changes.
		"""
		tabIdx = self.getCurrentTabID()

		# Update the zoom slider to the current zoom for this tab
		self.zoomScale.set(self.currZoom[tabIdx])

	def getCurrentTabID(self):
		"""
		Return the zero-based index of the currently selected tab in the main Notebook widget
		"""
		return self.nb.index( self.nb.select() )

ipa = IPA()
ipa.go()			# This call doesn't return until the application terminates