import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image
from PIL.ImageTk import PhotoImage 
from ScrolledCanvas import ScrolledCanvas
from IPAController import IPAController

class IPAView:

	def __init__(self, controller):
		self.model = []
		self.controller = controller
		self.LaunchUI()

	def LaunchUI(self):
		# Initialize persistent storage lists for images.  To Do - Code Smell...Make
		# an object storing all info about an image (MVC?)
		# self.pilImages = []		# store PIL image objects
		# self.tkImages = []		# store original tkInter PhotoImage objects
		# self.modTkImages = []	# store interim PhotoImage objects
		# self.imgCanvases = []	# store tkInter canvas objects (to enable changing the displayed image)
		# self.origSizes = []		# store (w,h) tuples with the original dimensions of each image
		# self.currZoom = []		# store the current zoom level for each image

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

		self.tintScale.update()						# if update not called, then the returned width will be 1
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
		return

	def onOpenButtonPress(self):
		"""
		Button handler:  Called when the Open... button is pressed
		"""
		# Display a file chooser
		filepath = filedialog.askopenfilename(initialdir = imgdir, title="Choose An Image to Open")

		# Open the chosen file (if any)
		# if filepath:
		# 	self.openImage(filepath)

	def onZoomMove(self, value):
		"""
		Event handler - the Zoom slider has moved. Scale the image on the current tab accordingly.
		"""
		# Get the active tab #.  Abort if no tabs
		try:
			tabIdx = self.getCurrentTabID()
		except:
			return

		# # remember the new zoom for this image
		# self.currZoom[tabIdx] = int(round(float(value)))

		# # scale the image
		# self.zoomImage(value)

	def dummy(self):
		return

	def go(self):
		self.mainFrame.mainloop()

	def onTabChanged(self, event):
		"""
		Event handler - called whenever the main Notebook's active tab selection changes.
		"""
		# tabIdx = self.getCurrentTabID()

		# # Update the zoom slider to the current zoom for this tab
		# self.zoomScale.set(self.currZoom[tabIdx])

