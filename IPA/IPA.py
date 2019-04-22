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
		self.mainFrame = tk.Frame(parent=None)
		self.mainFrame.pack()
		self.mainFrame.master.title("IPA: Image Processing Application")

		self.tkImages = []		# for aggregation of tkInter image objects
		
		self.nb = ttk.Notebook(self.mainFrame, padding=0) # height and width are for size of initial blank Notebook
		self.nb.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)

		self.closeButton = tk.Button(self.mainFrame, text="Close", command=self.onCloseButtonPress)
		self.saveButton = tk.Button(self.mainFrame, text="Save...", command=self.onSaveButtonPress, state='disabled')
		self.openButton = tk.Button(self.mainFrame, text='Open...', command=self.onOpenButtonPress)

		self.closeButton.pack(side=tk.RIGHT)
		self.saveButton.pack(side=tk.RIGHT)
		self.openButton.pack(side=tk.RIGHT)

		# To Do if time:  Can I improve the packing of the widgets so the buttons don't collapse away on vertical size-down?

	def go(self):
		"""
		Start the application running by firing off the tkInter event loop 
		"""
		self.mainFrame.mainloop()

	def onCloseButtonPress(self):
		"""
		Button handler:  Called when the Close button is pressed
		"""
		print("onCloseButtonPress()")
		# To Do - offer to save all unsaved edits
		self.mainFrame.quit()

	def onSaveButtonPress(self):
		"""
		Button handler:  Called when the Save... button is pressed
		"""
		print("onSaveButtonPress()")

	def onOpenButtonPress(self):
		"""
		Button handler:  Called when the Open... button is pressed
		"""
		# Display a file chooser
		filepath = filedialog.askopenfilename(initialdir = imgdir, title="Choose An Image to Open")
		print("onOpenButtonPress() chose",filepath)

		# Open the chosen file (if any)
		if filepath:
			self.openImage(filepath)

	def openImage(self, filepath):
		"""
		Open an image file and add a tab to display it.
		"""

		# Open the image file using PIL and save a reference to the image object (aggregation)
		tkImage = PhotoImage(image=Image.open(filepath))

		self.tkImages.append(tkImage)	# must keep a persistent reference so the image doesn't get garbage collected.

		# Add a tab to the main frame's notebook object, and display the image on that tab pane
		(_,filename) = os.path.split(filepath)	# pull out the filename to use as the tab title
		frame = tk.Frame(self.nb)
		self.nb.add(frame, text=filename)

		canvas = ScrolledCanvas(frame)

		# compute a maximum size based on the display size, leaving some buffer for other UI elements
		screenW = self.mainFrame.winfo_screenwidth()-40
		screenH = self.mainFrame.winfo_screenheight()-150

		# create the canvas object on which the image will be displayed
		canvas.config(width=min(screenW,tkImage.width()), height=min(screenH,tkImage.height()))	# size of the image region on screen
		canvas.config(scrollregion=(0, 0, tkImage.width(), tkImage.height()))					# virtual size of the image
		canvas.create_image(0, 0, image=tkImage, anchor=tk.NW)				 					# 0,0 is the relative coordinates of the image
		canvas.pack(fill=tk.BOTH)

		# Now we have at least one image open.  Enable the Save... button
		self.saveButton['state'] = 'normal'


ipa = IPA()
ipa.go()			# This call doesn't return until the application terminates